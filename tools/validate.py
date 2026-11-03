#!/usr/bin/env python3
"""Valida os bundles: conformidade OKF v0.2 + regras locais (spec/02, spec/03, spec/04, schema/ontology.yaml).

Uso: python tools/validate.py [--strict]
  --strict  trata conceitos com stale_after vencido como erro (padrão: aviso)
Sai com código 1 se houver erros.
"""
from __future__ import annotations

import datetime as dt
import re
import sys

import yaml

from memlib import (
    FOOTNOTE_DEF, FOOTNOTE_REF, ROOT, as_datetime, body_links, concepts_by_key, is_internal,
    key_for_path, load_docs, load_ontology, normalize_id, verified_list,
)

SECRET_PATTERNS = {
    "chave AWS": re.compile(r"AKIA[0-9A-Z]{16}"),
    "chave privada": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "token GitHub": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "token GitLab": re.compile(r"\bgl(pat|dt|rt|cbt|ptt|ft|imt|agent|oas|soat)-[A-Za-z0-9_-]{20,}"),
    "token Slack": re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}"),
    "chave de API": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
}
ACTOR = re.compile(r"^(human:[\w.@-]+|process:[\w.@-]+|[\w.-]+/[\w.:-]+)$")
LOG_DATE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$")
QUOTED = re.compile(r'["“][^"”]{3,}["”]')


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where, msg):
        self.errors.append(f"ERRO  {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"AVISO {where}: {msg}")


def where(d) -> str:
    return d.path.relative_to(ROOT).as_posix()


def has_human(fm: dict) -> bool:
    gen = fm.get("generated") or {}
    if isinstance(gen, dict) and str(gen.get("by", "")).startswith("human:"):
        return True
    return any(str(v.get("by", "")).startswith("human:") for v in verified_list(fm))


def check_reserved(onto, docs, r: Report):
    for d in docs:
        if d.kind == "index.md":
            is_root = d.path.parent == ROOT / d.bundle
            if d.fm is not None or d.error:
                if not is_root:
                    r.error(where(d), "index.md não pode ter frontmatter (OKF §8)")
                elif set((d.fm or {}).keys()) != {"okf_version"}:
                    r.error(where(d), "frontmatter do index.md raiz só pode ter okf_version (OKF §8, §12)")
                elif str(d.fm["okf_version"]) != onto["okf_version"]:
                    r.warn(where(d), f"okf_version {d.fm['okf_version']!r}; esperado {onto['okf_version']!r}")
            elif is_root:
                r.warn(where(d), "index.md raiz deveria declarar okf_version")
        elif d.kind == "log.md":
            if d.fm is not None:
                r.error(where(d), "log.md não pode ter frontmatter (OKF §9)")
            dates = []
            for line in d.body.splitlines():
                if line.startswith("## "):
                    m = LOG_DATE.match(line)
                    if not m:
                        r.error(where(d), f"cabeçalho de data fora do formato '## AAAA-MM-DD': {line!r}")
                    else:
                        dates.append(m.group(1))
            if dates != sorted(dates, reverse=True):
                r.warn(where(d), "datas do log devem estar da mais recente para a mais antiga")


def check_concepts(onto, docs, concepts, r: Report, strict: bool):
    types = onto["types"]
    now = dt.datetime.now(dt.timezone.utc)

    for d in docs:
        if d.kind != "concept":
            continue
        w = where(d)
        if d.error:
            r.error(w, d.error)
            continue
        if d.fm is None:
            r.error(w, "todo .md dentro de um bundle precisa de frontmatter com type (OKF §11)")
            continue
        fm, t = d.fm, d.type
        if not t:
            r.error(w, "type ausente (OKF §4.1)")
            continue
        if t not in types:
            r.error(w, f"type desconhecido: {t!r} (ver schema/ontology.yaml)")
            continue
        tdef = types[t] or {}
        status = fm.get("status", "stable")

        for f in sorted(set(fm) - set(onto["okf_fields"])):
            r.warn(w, f"campo fora da OKF: {f} (use só campos do padrão; ver spec/02)")
        for f in onto["required_fields"] + tdef.get("required", []):
            if fm.get(f) in (None, "", [], {}):
                r.error(w, f"campo obrigatório ausente: {f}")
        if "folder" in tdef and d.path.parent.name != tdef["folder"]:
            r.warn(w, f"type {t} costuma ficar na pasta {tdef['folder']}/")
        if status not in onto["enums"]["status"]:
            r.error(w, f"status inválido: {status!r} (draft | stable | deprecated)")

        # generated / verified (OKF §5.2, §7)
        gen = fm.get("generated")
        if gen is not None:
            if not isinstance(gen, dict) or not gen.get("by"):
                r.error(w, "generated precisa de by (OKF §5.2)")
            else:
                if not ACTOR.match(str(gen["by"])):
                    r.error(w, f"generated.by fora da convenção de ator: {gen['by']!r} (OKF §7)")
                if "at" in gen and not as_datetime(gen["at"]):
                    r.error(w, "generated.at deve ser ISO 8601 com fuso (ex.: 2026-10-30T15:00:00Z)")
        for i, v in enumerate(verified_list(fm)):
            if not v.get("by") or not ACTOR.match(str(v["by"])):
                r.error(w, f"verified[{i}].by ausente ou fora da convenção de ator")
            if not as_datetime(v.get("at")):
                r.error(w, f"verified[{i}].at deve ser ISO 8601 com fuso")

        # stale_after (OKF §5.5)
        stale = fm.get("stale_after")
        if stale is not None:
            st = as_datetime(stale)
            if not st:
                r.error(w, "stale_after deve ser ISO 8601 com fuso")
            elif now >= st:
                (r.error if strict else r.warn)(w, f"desatualizado desde {st:%Y-%m-%d}: reverifique e renove, ou remova")
        agent_written = isinstance(gen, dict) and not str(gen.get("by", "")).startswith(("human:", "process:"))
        if agent_written and not verified_list(fm) and stale is None:
            r.error(w, "conceito gerado por agente e sem verified precisa de stale_after")

        # regras de humano (spec/04)
        if status != "draft":
            if tdef.get("requires_human") and not has_human(fm):
                r.error(w, f"{t} não-draft exige human: em generated.by ou verified")
            risky = set(fm.get("tags") or []) & set(onto["human_required_tags"])
            if risky and not any(str(v.get("by", "")).startswith("human:") for v in verified_list(fm)):
                r.error(w, f"tags {sorted(risky)} exigem verified por human: (ou status draft)")

        # sources (OKF §5.1)
        sources = fm.get("sources") or []
        if not isinstance(sources, list):
            r.error(w, "sources deve ser uma lista")
            sources = []
        ids = set()
        for i, s in enumerate(sources):
            if not isinstance(s, dict) or not s.get("resource"):
                r.error(w, f"sources[{i}] precisa de resource (OKF §5.1)")
                continue
            if s.get("id"):
                ids.add(str(s["id"]))
            if "last_modified" in s and not as_datetime(s["last_modified"]):
                r.error(w, f"sources[{i}].last_modified deve ser ISO 8601 com fuso")
            res = str(s["resource"])
            if is_internal(res) and d.bundle + normalize_id(res) not in concepts:
                r.error(w, f"sources[{i}].resource aponta para conceito inexistente: {res}")
        defs = dict(FOOTNOTE_DEF.findall(d.body))
        for ref in set(FOOTNOTE_REF.findall(d.body)):
            if ref not in ids:
                r.error(w, f"nota de rodapé [^{ref}] sem sources[].id correspondente (OKF §5.1)")
            if ref not in defs:
                r.error(w, f"nota de rodapé [^{ref}] usada sem definição ([^{ref}]: ...)")
        if tdef.get("requires_quote") and not any(QUOTED.search(v) for v in defs.values()):
            r.error(w, f'{t} exige ao menos uma nota de rodapé com trecho literal entre aspas ([^id]: Título: "trecho")')

        # seções
        for section in tdef.get("sections", []):
            if not re.search(rf"^#{{1,2}}\s+{re.escape(section)}\s*$", d.body, re.MULTILINE):
                r.error(w, f"seção obrigatória ausente: # {section}")

        if t == "Decision" and status == "deprecated":
            links = {key_for_path(p, d.bundle) for _, p in body_links(d)}
            if not any(k in concepts and concepts[k].type == "Decision" for k in links):
                r.warn(w, "Decision deprecated sem link para a decisão que a substitui")

    # links do corpo (todos os .md dos bundles)
    for d in docs:
        for href, path in body_links(d):
            if not path.exists():
                r.error(where(d), f"link quebrado no corpo: {href}")


def check_evals(onto, concepts, r: Report):
    graders = onto["enums"]["grader"]
    seen: dict[str, str] = {}
    for bundle in onto["bundles"]:
        for path in sorted((ROOT / bundle).rglob("*.yaml")):
            if "evals" not in path.relative_to(ROOT / bundle).parts:
                continue
            w = path.relative_to(ROOT).as_posix()
            try:
                items = yaml.safe_load(path.read_text(encoding="utf-8")) or []
            except yaml.YAMLError as e:
                r.error(w, f"YAML inválido: {e}")
                continue
            if not isinstance(items, list):
                r.error(w, "arquivo de eval deve ser uma lista")
                continue
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    r.error(w, f"item {i} não é um mapa")
                    continue
                for f in ("id", "question", "answer", "grader", "source"):
                    if not item.get(f):
                        r.error(w, f"item {i} sem campo {f}")
                if item.get("grader") and item["grader"] not in graders:
                    r.error(w, f"item {item.get('id', i)}: grader inválido {item['grader']!r}")
                eid = item.get("id")
                if eid in seen:
                    r.error(w, f"id de eval duplicado: {eid} (também em {seen[eid]})")
                elif eid:
                    seen[eid] = w
                for cref in item.get("concepts") or []:
                    if bundle + normalize_id(str(cref)) not in concepts:
                        r.error(w, f"item {eid}: conceito inexistente {cref}")


def check_secrets(r: Report):
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix not in (".md", ".yaml", ".yml", ".json"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                r.error(path.relative_to(ROOT).as_posix(), f"possível segredo ({name}); remova e rotacione a credencial")


def main() -> int:
    strict = "--strict" in sys.argv
    onto = load_ontology()
    docs = load_docs(onto)
    concepts = concepts_by_key(docs)
    r = Report()
    check_reserved(onto, docs, r)
    check_concepts(onto, docs, concepts, r, strict)
    check_evals(onto, concepts, r)
    check_secrets(r)
    for line in r.warnings + r.errors:
        print(line)
    print(f"\n{len(concepts)} conceitos em {len(onto['bundles'])} bundles · {len(r.errors)} erros · {len(r.warnings)} avisos")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
