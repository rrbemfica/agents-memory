"""Leitura dos bundles OKF v0.2 e da ontologia, compartilhada por validate.py e build_graph.py."""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
FOOTNOTE_REF = re.compile(r"\[\^([^\]]+)\](?!:)")
FOOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$", re.MULTILINE)
RESERVED = ("index.md", "log.md")


@dataclass
class Doc:
    bundle: str                  # caminho do bundle a partir da raiz do repo (ex.: "knowledge")
    path: Path
    fm: dict | None = None       # None = sem frontmatter
    body: str = ""
    error: str | None = None     # erro de parse do frontmatter

    @property
    def id(self) -> str:
        """ID OKF: caminho dentro do bundle, sem .md, com '/' inicial."""
        rel = self.path.relative_to(ROOT / self.bundle).as_posix()
        return "/" + rel[:-3]

    @property
    def key(self) -> str:
        """Identificador único no repo (bundle + ID)."""
        return self.bundle + self.id

    @property
    def kind(self) -> str:
        return self.path.name if self.path.name in RESERVED else "concept"

    @property
    def type(self) -> str | None:
        return (self.fm or {}).get("type")


def load_ontology() -> dict:
    return yaml.safe_load((ROOT / "schema" / "ontology.yaml").read_text(encoding="utf-8"))


def parse(path: Path) -> tuple[dict | None, str, str | None]:
    """Retorna (frontmatter ou None, corpo, erro)."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER.match(text)
    if not m:
        return None, text, None
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return None, m.group(2), f"frontmatter inválido: {e}"
    if not isinstance(fm, dict):
        return None, m.group(2), "frontmatter não é um mapa"
    return fm, m.group(2), None


def load_docs(ontology: dict) -> list[Doc]:
    docs = []
    for bundle in ontology["bundles"]:
        base = ROOT / bundle
        for path in sorted(base.rglob("*.md")):
            fm, body, err = parse(path)
            docs.append(Doc(bundle, path, fm, body, err))
    return docs


def concepts_by_key(docs: list[Doc]) -> dict[str, Doc]:
    return {d.key: d for d in docs if d.kind == "concept" and d.fm is not None}


def normalize_id(ref: str) -> str:
    """'/a/b.md' ou '/a/b' -> '/a/b'."""
    ref = ref.split("#", 1)[0]
    return ref[:-3] if ref.endswith(".md") else ref


def is_internal(ref: str) -> bool:
    return isinstance(ref, str) and ref.startswith("/")


def internal_sources(d: Doc) -> list[str]:
    """IDs de conceitos citados em sources[].resource (fontes dentro do mesmo bundle)."""
    out = []
    for s in (d.fm or {}).get("sources") or []:
        if isinstance(s, dict) and is_internal(s.get("resource")):
            out.append(normalize_id(s["resource"]))
    return out


def resolve_link(d: Doc, href: str) -> Path | None:
    """Resolve um link do corpo para um caminho no disco (None se externo)."""
    if "://" in href or href.startswith(("mailto:", "#")):
        return None
    target = href.split("#", 1)[0]
    if not target:
        return None
    if target.startswith("/"):
        return (ROOT / d.bundle / target.lstrip("/")).resolve()
    return (d.path.parent / target).resolve()


def body_links(d: Doc) -> list[tuple[str, Path]]:
    out = []
    for href in MD_LINK.findall(d.body):
        p = resolve_link(d, href)
        if p is not None:
            out.append((href, p))
    return out


def key_for_path(path: Path, bundle: str) -> str | None:
    """Converte caminho de arquivo .md dentro do bundle em chave de conceito."""
    try:
        rel = path.relative_to(ROOT / bundle).as_posix()
    except ValueError:
        return None
    if not rel.endswith(".md") or rel.split("/")[-1] in RESERVED:
        return None
    return bundle + "/" + rel[:-3]


def verified_list(fm: dict) -> list[dict]:
    v = fm.get("verified")
    if v is None:
        return []
    if isinstance(v, dict):          # OKF §5.2: mapa único = lista de um item
        return [v]
    return [x for x in v if isinstance(x, dict)] if isinstance(v, list) else []


def trust_tier(fm: dict) -> str:
    """OKF §5.3."""
    vs = verified_list(fm)
    if not vs:
        return "unverified"
    if any(str(x.get("by", "")).startswith("human:") for x in vs):
        return "human-reviewed"
    return "machine-confirmed"


def as_datetime(value) -> dt.datetime | None:
    """Aceita datetime com fuso (o YAML já converte) ou string ISO 8601 com fuso."""
    if isinstance(value, dt.datetime):
        return value if value.tzinfo else None
    if isinstance(value, str):
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed if parsed.tzinfo else None
    return None
