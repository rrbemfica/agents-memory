#!/usr/bin/env python3
"""Valida os bundles contra spec/02-formato.md, spec/03-tipos.md e schema/ontology.yaml.

Uso: python tools/validate.py [--strict]
  --strict  trata conceitos expirados como erro (padrão: aviso)
Sai com código 1 se houver erros.
"""
from __future__ import annotations

import datetime as dt
import re
import sys

import yaml

from memlib import ROOT, body_links, bundle_files, concept_id, load_concepts, load_ontology, relations_of

SECRET_PATTERNS = {
    "chave AWS": re.compile(r"AKIA[0-9A-Z]{16}"),
    "chave privada": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "token GitHub": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "token Slack": re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}"),
    "chave de API": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"),
}
LOCAL_REF = re.compile(r"^[\w./-]+\.md$")


class Report:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str):
        self.errors.append(f"ERRO  {where}: {msg}")

    def warn(self, where: str, msg: str):
        self.warnings.append(f"AVISO {where}: {msg}")


def as_date(value) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value[:10])
        except ValueError:
            return None
    return None


def allowed(spec_value, type_name: str | None) -> bool:
    return spec_value == "*" or type_name in spec_value


def check_concepts(onto: dict, concepts: dict, r: Report, strict: bool):
    types = onto["types"]
    enums = onto["enums"]
    rel_spec = onto["relations"]
    today = dt.date.today()
    superseded_targets = {t for c in concepts.values() for n, t in relations_of(c) if n == "supersedes"}

    for cid, c in concepts.items():
        t = c.type
        if t not in types:
            r.error(cid, f"type desconhecido: {t!r} (ver schema/ontology.yaml)")
            continue
        tdef = types[t] or {}

        # nome reservado / pasta
        if "filename" in tdef and c.path.name != tdef["filename"]:
            r.error(cid, f"type {t} deve estar em um arquivo {tdef['filename']}")
        if c.path.name in ("index.md", "log.md"):
            expected = "Domain" if c.path.name == "index.md" else "Log"
            if t != expected:
                r.error(cid, f"{c.path.name} é reservado para type {expected}")
        if "folder" in tdef and c.path.parent.name != tdef["folder"]:
            r.warn(cid, f"type {t} costuma ficar na pasta {tdef['folder']}/")

        # campos obrigatórios
        required = list(onto["fields"]["base"])
        if t != "Log":
            required += onto["fields"]["described"]
        if t not in ("Domain", "Log"):
            required += onto["fields"]["concept"]
        required += tdef.get("required", [])
        for f in required:
            if c.fm.get(f) in (None, "", []):
                r.error(cid, f"campo obrigatório ausente: {f}")

        if t in ("Domain", "Log"):
            continue

        # enums
        if c.fm.get("status") and c.fm["status"] not in enums["status"]:
            r.error(cid, f"status inválido: {c.fm['status']!r}")
        if c.fm.get("trust") and c.fm["trust"] not in enums["trust"]:
            r.error(cid, f"trust inválido: {c.fm['trust']!r}")

        # expiração
        needs_expiry = c.fm.get("trust") == "inferred" or t == "Meeting"
        expires = as_date(c.fm.get("expires"))
        if needs_expiry and not expires:
            r.error(cid, "trust inferred e Meeting exigem expires (AAAA-MM-DD)")
        if expires and expires < today:
            (r.error if strict else r.warn)(cid, f"expirado em {expires}: renove (se confirmado) ou remova")

        # fontes
        sources = c.fm.get("sources") or []
        if not isinstance(sources, list):
            r.error(cid, "sources deve ser uma lista")
            sources = []
        for i, s in enumerate(sources):
            if not isinstance(s, dict) or not s.get("kind") or not s.get("ref"):
                r.error(cid, f"sources[{i}] precisa de kind e ref")
                continue
            if s["kind"] not in enums["source_kind"]:
                r.error(cid, f"sources[{i}].kind inválido: {s['kind']!r}")
            ref = str(s["ref"])
            if LOCAL_REF.match(ref) and not (ROOT / ref).exists():
                r.error(cid, f"sources[{i}].ref aponta para arquivo inexistente: {ref}")
        if t == "Decision" and not any(isinstance(s, dict) and s.get("quote") for s in sources):
            r.error(cid, "Decision exige ao menos uma fonte com quote literal")

        # relações
        for name, target in relations_of(c):
            if name not in rel_spec:
                r.error(cid, f"relação desconhecida: {name}")
                continue
            if not allowed(rel_spec[name]["from"], t):
                r.error(cid, f"relação {name} não pode sair de {t}")
            if target not in concepts:
                r.error(cid, f"relação {name} aponta para conceito inexistente: {target}")
            elif not allowed(rel_spec[name]["to"], concepts[target].type):
                r.error(cid, f"relação {name} não pode apontar para {concepts[target].type} ({target})")

        # seções e tamanho
        for section in tdef.get("sections", []):
            if not re.search(rf"^##\s+{re.escape(section)}\s*$", c.body, re.MULTILINE):
                r.error(cid, f"seção obrigatória ausente: ## {section}")
        words = len(c.body.split())
        if words > onto["limits"]["body_words_warn"]:
            r.warn(cid, f"corpo com {words} palavras; considere quebrar em conceitos menores")

        if t == "Decision" and c.fm.get("status") == "superseded" and cid not in superseded_targets:
            r.warn(cid, "Decision superseded sem nenhuma outra declarando supersedes para ela")

    # links do corpo (todos os arquivos, inclusive index/log)
    for cid, c in concepts.items():
        for target in body_links(c):
            if not (ROOT / target).exists():
                r.error(cid, f"link quebrado no corpo: {target}")
        if c.type == "Domain":
            lines = len(c.body.splitlines())
            if lines > onto["limits"]["index_lines_warn"]:
                r.warn(cid, f"index.md com {lines} linhas; mantenha a porta de entrada enxuta")


def check_logs(onto: dict, concepts: dict, r: Report):
    actions = onto["enums"]["log_action"]
    for cid, c in concepts.items():
        if c.type != "Log":
            continue
        for n, line in enumerate(c.body.splitlines(), 1):
            if not line.startswith("- "):
                continue
            parts = [p.strip() for p in line[2:].split("·")]
            if len(parts) < 4 or parts[1] not in actions:
                r.warn(cid, f"linha {n} fora do formato 'data · ação · conceito · time · motivo'")


def check_evals(onto: dict, concepts: dict, r: Report):
    graders = onto["enums"]["grader"]
    seen: dict[str, str] = {}
    for path in bundle_files(onto, ".yaml"):
        if path.parent.name != "evals" and path.parent.parent.name != "evals":
            continue
        where = concept_id(path)
        try:
            items = yaml.safe_load(path.read_text(encoding="utf-8")) or []
        except yaml.YAMLError as e:
            r.error(where, f"YAML inválido: {e}")
            continue
        if not isinstance(items, list):
            r.error(where, "arquivo de eval deve ser uma lista")
            continue
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                r.error(where, f"item {i} não é um mapa")
                continue
            for f in ("id", "question", "answer", "grader", "source"):
                if not item.get(f):
                    r.error(where, f"item {i} sem campo {f}")
            if item.get("grader") and item["grader"] not in graders:
                r.error(where, f"item {item.get('id', i)}: grader inválido {item['grader']!r}")
            eid = item.get("id")
            if eid in seen:
                r.error(where, f"id de eval duplicado: {eid} (também em {seen[eid]})")
            elif eid:
                seen[eid] = where
            for cref in item.get("concepts") or []:
                if cref not in concepts:
                    r.error(where, f"item {eid}: conceito inexistente {cref}")


def check_secrets(r: Report):
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix not in (".md", ".yaml", ".yml", ".json"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                r.error(concept_id(path), f"possível segredo ({name}); remova e rotacione a credencial")


def main() -> int:
    strict = "--strict" in sys.argv
    onto = load_ontology()
    concepts, parse_errors = load_concepts(onto)
    r = Report()
    for cid, err in parse_errors:
        r.error(cid, err)
    check_concepts(onto, concepts, r, strict)
    check_logs(onto, concepts, r)
    check_evals(onto, concepts, r)
    check_secrets(r)

    for line in r.warnings + r.errors:
        print(line)
    print(f"\n{len(concepts)} conceitos · {len(r.errors)} erros · {len(r.warnings)} avisos")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
