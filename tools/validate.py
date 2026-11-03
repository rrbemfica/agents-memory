#!/usr/bin/env python3
"""Valida os bundles contra a OKF v0.2 e confere as recomendações deste repo.

ERRO  = viola a OKF v0.2 ou vaza segredo. Faz o CI falhar.
AVISO = recomendação nossa (spec/02 a spec/05, schema/ontology.yaml). Não faz o CI falhar.

Uso: python tools/validate.py [--strict]
  --strict  stale_after vencido vira erro nos bundles de strict_bundles (usado só na rodada agendada)
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
                        r.error(where(d), f"cabeçalho de data fora do formato '## AAAA-MM-DD' (OKF §9): {line!r}")
                    else:
                        dates.append(m.group(1))
            if dates != sorted(dates, reverse=True):
                r.warn(where(d), "datas do log devem estar da mais recente para a mais antiga")


def check_okf_fields(fm: dict, w: str, r: Report, statuses: list[str]):
    """Formato dos campos definidos pela OKF v0.2. Violação é erro."""
    status = fm.get("status", "stable")
    if status not in statuses:
        r.error(w, f"status inválido: {status!r} (draft | stable | deprecated, OKF §5.4)")
    gen = fm.get("generated")
    if gen is not None:
        if not isinstance(gen, dict) or not gen.get("by"):
            r.error(w, "generated precisa de by (OKF §5.2)")
        elif "at" in gen and not as_datetime(gen["at"]):
            r.error(w, "generated.at deve ser ISO 8601 com fuso, ex.: 2026-10-30T15:00:00Z (OKF §5.2)")
    for i, v in enumerate(verified_list(fm)):
        if not v.get("by"):
            r.error(w, f"verified[{i}] precisa de by (OKF §5.2)")
        if not as_datetime(v.get("at")):
            r.error(w, f"verified[{i}].at deve ser ISO 8601 com fuso (OKF §5.2)")
    if "stale_after" in fm and not as_datetime(fm["stale_after"]):
        r.error(w, "stale_after deve ser ISO 8601 com fuso (OKF §5.5)")
    sources = fm.get("sources")
    if sources is not None and not isinstance(sources, list):
        r.error(w, "sources deve ser uma lista (OKF §5.1)")
    for i, s in enumerate(sources if isinstance(sources, list) else []):
        if not isinstance(s, dict) or not s.get("resource"):
            r.error(w, f"sources[{i}] precisa de resource (OKF §5.1)")
        elif "last_modified" in s and not as_datetime(s["last_modified"]):
            r.error(w, f"sources[{i}].last_modified deve ser ISO 8601 com fuso (OKF §5.1)")


def check_recommendations(onto, d, concepts, r: Report, strict: bool, now: dt.datetime):
    """Recomendações deste repo. Violação é aviso (exceto --strict para stale_after)."""
    fm, t, w = d.fm, d.type, where(d)
    tdef = onto["types"].get(t, None)
    if t not in onto["types"]:
        r.warn(w, f"type {t!r} fora do vocabulário recomendado (schema/ontology.yaml)")
    tdef = tdef or {}
    status = fm.get("status", "stable")

    for f in sorted(set(fm) - set(onto["okf_fields"])):
        r.warn(w, f"campo {f} não é usado neste repo (recomendamos só campos da OKF; ver spec/02)")
    for f in onto["recommended_fields"] + tdef.get("recommended", []):
        if fm.get(f) in (None, "", [], {}):
            r.warn(w, f"campo recomendado ausente: {f}")
    if "folder" in tdef and d.path.parent.name != tdef["folder"]:
        r.warn(w, f"type {t} costuma ficar na pasta {tdef['folder']}/")

    gen = fm.get("generated")
    actors = [gen.get("by") if isinstance(gen, dict) else None] + [v.get("by") for v in verified_list(fm)]
    for actor in actors:
        if actor and not ACTOR.match(str(actor)):
            r.warn(w, f"ator fora da convenção human:<id> | process:<id> | <produtor>/<versão>: {actor!r} (OKF §7)")

    stale = as_datetime(fm.get("stale_after"))
    if stale and now >= stale:
        escalate = strict and d.bundle in onto["strict_bundles"]
        (r.error if escalate else r.warn)(w, f"desatualizado desde {stale:%Y-%m-%d}: reverifique e renove, ou remova")
    agent_written = isinstance(gen, dict) and not str(gen.get("by", "")).startswith(("human:", "process:"))
    if agent_written and not verified_list(fm) and "stale_after" not in fm:
        r.warn(w, "conceito escrito por agente e sem verified: recomendamos stale_after")

    if status != "draft":
        if tdef.get("human_review") and not has_human(fm):
            r.warn(w, f"{t} fora de draft sem human: em generated.by ou verified (ver spec/04)")
        risky = set(fm.get("tags") or []) & set(onto["human_review_tags"])
        if risky and not any(str(v.get("by", "")).startswith("human:") for v in verified_list(fm)):
            r.warn(w, f"tags {sorted(risky)}: recomendamos verified por human: ou status draft (ver spec/04)")

    sources = fm.get("sources") if isinstance(fm.get("sources"), list) else []
    ids = {str(s["id"]) for s in sources if isinstance(s, dict) and s.get("id")}
    for s in sources:
        res = s.get("resource") if isinstance(s, dict) else None
        if is_internal(res) and d.bundle + normalize_id(res) not in concepts:
            r.warn(w, f"fonte aponta para conceito inexistente: {res}")
    defs = dict(FOOTNOTE_DEF.findall(d.body))
    for ref in sorted(set(FOOTNOTE_REF.findall(d.body))):
        if ref not in ids:
            r.warn(w, f"nota de rodapé [^{ref}] sem sources[].id correspondente (OKF §5.1)")
        if ref not in defs:
            r.warn(w, f"nota de rodapé [^{ref}] usada sem definição ([^{ref}]: ...)")
    if tdef.get("quote") and not any(QUOTED.search(v) for v in defs.values()):
        r.warn(w, f'{t}: recomendamos ao menos uma nota de rodapé com trecho literal ([^id]: Título: "trecho")')

    for section in tdef.get("sections", []):
        if not re.search(rf"^#{{1,2}}\s+{re.escape(section)}\s*$", d.body, re.MULTILINE):
            r.warn(w, f"seção recomendada ausente: # {section}")

    if t == "Decision" and status == "deprecated":
        links = {key_for_path(p, d.bundle) for _, p in body_links(d)}
        if not any(k in concepts and concepts[k].type == "Decision" for k in links):
            r.warn(w, "Decision deprecated sem link para a decisão que a substitui")


def check_concepts(onto, docs, concepts, r: Report, strict: bool):
    now = dt.datetime.now(dt.timezone.utc)
    for d in docs:
        if d.kind != "concept":
            continue
        w = where(d)
        if d.error:
            r.error(w, d.error)
        elif d.fm is None:
            r.error(w, "todo .md dentro de um bundle precisa de frontmatter com type (OKF §11)")
        elif not d.type:
            r.error(w, "type ausente (OKF §4.1)")
        else:
            check_okf_fields(d.fm, w, r, onto["enums"]["status"])
            check_recommendations(onto, d, concepts, r, strict, now)

    # links do corpo: a OKF tolera link quebrado, então é só aviso
    for d in docs:
        root = (ROOT / d.bundle).resolve()
        for href, path in body_links(d):
            if not path.is_relative_to(root):
                r.warn(where(d), f"link relativo sai do bundle (quebra se o bundle for distribuído sozinho): {href}")
            elif not path.exists():
                r.warn(where(d), f"link quebrado: {href}")


def check_evals(onto, concepts, r: Report):
    """Evals são camada nossa (spec/05): problemas viram aviso."""
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
                r.warn(w, f"YAML inválido: {e}")
                continue
            if not isinstance(items, list):
                r.warn(w, "arquivo de eval deve ser uma lista")
                continue
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    r.warn(w, f"item {i} não é um mapa")
                    continue
                for f in ("id", "question", "answer", "grader", "source"):
                    if not item.get(f):
                        r.warn(w, f"item {i} sem campo {f}")
                if item.get("grader") and item["grader"] not in graders:
                    r.warn(w, f"item {item.get('id', i)}: grader inválido {item['grader']!r}")
                eid = item.get("id")
                if eid in seen:
                    r.warn(w, f"id de eval duplicado: {eid} (também em {seen[eid]})")
                elif eid:
                    seen[eid] = w
                for cref in item.get("concepts") or []:
                    if bundle + normalize_id(str(cref)) not in concepts:
                        r.warn(w, f"item {eid}: conceito inexistente {cref}")


def check_secrets(r: Report):
    """Fora da OKF, mas segredo no repo é incidente de segurança: continua erro."""
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
