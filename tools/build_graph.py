#!/usr/bin/env python3
"""Gera graph/ a partir dos bundles: graph.json, backlinks.json e um Mermaid por área.

Só usa o que a OKF v0.2 define: links do corpo (aresta `link`) e fontes internas em
sources[].resource (aresta `source`). Arestas não têm tipo de negócio; o sentido está no texto.

Uso: python tools/build_graph.py
graph/ não é versionado: serve para olhar localmente e como artefato do CI.
A saída é determinística (ordenada, sem datas relativas a "hoje").
"""
from __future__ import annotations

import json
from collections import defaultdict

from memlib import ROOT, body_links, concepts_by_key, internal_sources, key_for_path, load_docs, load_ontology, trust_tier

INVERSE = {"link": "linkedFrom", "source": "citedBy"}
SHAPES = {
    "Decision": ('{{"', '"}}'),
    "Service": ('[("', '")]'),
    "Term": ('("', '")'),
    "Incident": ('>"', '"]'),
}


def area_of(bundle: str, cid: str) -> str:
    """knowledge: org | domains/<nome>; outros bundles: o próprio bundle."""
    parts = cid.strip("/").split("/")
    if bundle == "knowledge":
        if parts[0] == "domains" and len(parts) > 2:
            return f"knowledge/domains/{parts[1]}"
        return f"knowledge/{parts[0]}"
    return bundle


def build():
    onto = load_ontology()
    docs = load_docs(onto)
    concepts = concepts_by_key(docs)

    nodes = {}
    for key, d in sorted(concepts.items()):
        stale = d.fm.get("stale_after")
        nodes[key] = {
            "bundle": d.bundle,
            "id": d.id,
            "area": area_of(d.bundle, d.id),
            "type": d.type,
            "title": d.fm.get("title"),
            "status": d.fm.get("status", "stable"),
            "trust": trust_tier(d.fm),
            "stale_after": stale.isoformat() if hasattr(stale, "isoformat") else stale,
        }

    edges = set()
    for key, d in concepts.items():
        for target in internal_sources(d):
            tk = d.bundle + target
            if tk in nodes:
                edges.add((key, "source", tk))
        cited = {t for s, r, t in edges if s == key}
        for _, path in body_links(d):
            tk = key_for_path(path, d.bundle)
            if tk and tk in nodes and tk != key and tk not in cited:
                edges.add((key, "link", tk))
    edges = sorted(edges)

    backlinks = defaultdict(list)
    for src, rel, dst in edges:
        backlinks[dst].append({"from": src, "rel": INVERSE[rel]})

    out = ROOT / "graph"
    out.mkdir(exist_ok=True)
    (out / "graph.json").write_text(
        json.dumps({"nodes": nodes, "edges": [{"from": s, "rel": r, "to": t} for s, r, t in edges]},
                   indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "backlinks.json").write_text(
        json.dumps(dict(sorted(backlinks.items())), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    areas = sorted({n["area"] for n in nodes.values()})
    written = set()
    for area in areas:
        members = [k for k, n in nodes.items() if n["area"] == area]
        ids = {k: f"n{i}" for i, k in enumerate(members)}
        lines = ["```mermaid", "graph LR", "  classDef unverified stroke-dasharray: 5 5", "  classDef deprecated opacity:0.5"]
        for k in members:
            n = nodes[k]
            left, right = SHAPES.get(n["type"], ('["', '"]'))
            label = str(n["title"] or n["id"]).replace('"', "'")
            lines.append(f"  {ids[k]}{left}{label}{right}")
            if n["status"] == "deprecated":
                lines.append(f"  class {ids[k]} deprecated")
            elif n["trust"] == "unverified":
                lines.append(f"  class {ids[k]} unverified")
        for src, rel, dst in edges:
            if src in ids and dst in ids:
                arrow = "-. fonte .->" if rel == "source" else "-->"
                lines.append(f"  {ids[src]} {arrow} {ids[dst]}")
        lines.append("```")
        name = area.replace("/", "--") + ".md"
        header = (f"# Grafo · {area}\n\n> Gerado por `tools/build_graph.py` (não versionado). "
                  "Seta cheia = link no texto · pontilhada = fonte · tracejado = não verificado · esmaecido = deprecated.\n\n")
        (out / name).write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
        written.add(name)

    for p in out.glob("*.md"):
        if p.name not in written:
            p.unlink()

    print(f"{len(nodes)} nós · {len(edges)} arestas · {len(areas)} áreas → graph/")


if __name__ == "__main__":
    build()
