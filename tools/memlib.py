"""Leitura dos bundles e da ontologia, compartilhada por validate.py e build_graph.py."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


@dataclass
class Concept:
    id: str                      # caminho a partir da raiz do repo (identidade OKF)
    path: Path
    fm: dict = field(default_factory=dict)
    body: str = ""

    @property
    def type(self) -> str | None:
        return self.fm.get("type")

    @property
    def bundle(self) -> str:
        parts = Path(self.id).parts
        return parts[0] if parts[0] == "org" else "/".join(parts[:2])


def load_ontology() -> dict:
    return yaml.safe_load((ROOT / "schema" / "ontology.yaml").read_text(encoding="utf-8"))


def bundle_files(ontology: dict, suffix: str) -> list[Path]:
    files = []
    for root in ontology["bundle_roots"]:
        base = ROOT / root
        if base.exists():
            files += [p for p in base.rglob(f"*{suffix}") if p.is_file()]
    return sorted(files)


def concept_id(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse(path: Path) -> tuple[dict | None, str, str | None]:
    """Retorna (frontmatter, corpo, erro)."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    if not m:
        return None, text, "sem frontmatter YAML"
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return None, m.group(2), f"frontmatter inválido: {e}"
    if not isinstance(fm, dict):
        return None, m.group(2), "frontmatter não é um mapa"
    return fm, m.group(2), None


def load_concepts(ontology: dict) -> tuple[dict[str, Concept], list[tuple[str, str]]]:
    """Carrega todos os .md dos bundles (exceto README.md). Retorna (conceitos, erros de parse)."""
    concepts, errors = {}, []
    for path in bundle_files(ontology, ".md"):
        if path.name == "README.md":
            continue
        cid = concept_id(path)
        fm, body, err = parse(path)
        if err:
            errors.append((cid, err))
            continue
        concepts[cid] = Concept(cid, path, fm, body)
    return concepts, errors


def relations_of(c: Concept) -> list[tuple[str, str]]:
    """Lista (relação, alvo) declaradas no frontmatter."""
    rels = c.fm.get("relations") or {}
    out = []
    if isinstance(rels, dict):
        for name, targets in rels.items():
            for t in targets or []:
                if isinstance(t, str):
                    out.append((name, t))
    return out


def body_links(c: Concept) -> list[str]:
    """Links Markdown locais do corpo, resolvidos para IDs (sem âncora)."""
    out = []
    for href in MD_LINK.findall(c.body):
        if "://" in href or href.startswith(("mailto:", "#")):
            continue
        target = (c.path.parent / href.split("#", 1)[0]).resolve()
        try:
            out.append(target.relative_to(ROOT).as_posix())
        except ValueError:
            out.append(href)  # aponta para fora do repo
    return out
