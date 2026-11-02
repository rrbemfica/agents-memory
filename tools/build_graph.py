#!/usr/bin/env python3
"""Gera graph/ a partir dos bundles: graph.json, backlinks.json e um Mermaid por bundle.

Uso: python tools/build_graph.py
A saída é determinística (ordenada) para que o CI possa checar se está atualizada.
"""
from __future__ import annotations

import json
from collections import defaultdict

from memlib import ROOT, body_links, load_concepts, load_ontology, relations_of

# Relações omitidas do diagrama para não poluir (continuam no graph.json)
HIDDEN_IN_DIAGRAM = {"partOf", "mentions"}
SHAPES = {
    "Domain": ('(["', '"])'),
    "Decision": ('{{"', '"}}'),
    "Service": ('[("', '")]'),
    "Term": ('("', '")'),
    "Incident": ('>"', '"]'),
}


def build():
    onto = load_ontology()
    concepts, _ = load_concepts(onto)
    inverse = onto["inverse"]

    nodes = {
        cid: {
            "type": c.type,
            "title": c.fm.get("title"),
            "status": c.fm.get("status"),
            "trust": c.fm.get("trust"),
            "owner": c.fm.get("owner"),
            "bundle": c.bundle,
        }
        for cid, c in sorted(concepts.items())
        if c.type != "Log"
    }

    edges = set()
    for cid, c in concepts.items():
        if cid not in nodes:
            continue
        for rel, target in relations_of(c):
            if target in nodes:
                edges.add((cid, rel, target))
        declared = {t for _, t in relations_of(c)}
        for target in body_links(c):
            if target in nodes and target != cid and target not in declared:
                edges.add((cid, "mentions", target))
    edges = sorted(edges)

    backlinks = defaultdict(list)
    for src, rel, dst in edges:
        backlinks[dst].append({"from": src, "rel": inverse.get(rel, "mentionedBy")})

    out = ROOT / "graph"
    out.mkdir(exist_ok=True)
    (out / "graph.json").write_text(
        json.dumps(
            {"nodes": nodes, "edges": [{"from": s, "rel": r, "to": d} for s, r, d in edges]},
            indent=2, ensure_ascii=False, default=str,
        ) + "\n",
        encoding="utf-8",
    )
    (out / "backlinks.json").write_text(
        json.dumps(dict(sorted(backlinks.items())), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    bundles = sorted({n["bundle"] for n in nodes.values()})
    for bundle in bundles:
        members = [cid for cid, n in nodes.items() if n["bundle"] == bundle]
        ids = {cid: f"n{i}" for i, cid in enumerate(members)}
        lines = ["```mermaid", "graph LR"]
        for cid in members:
            n = nodes[cid]
            left, right = SHAPES.get(n["type"], ('["', '"]'))
            label = str(n["title"] or cid).replace('"', "'")
            if n["status"] == "superseded":
                label += " (superseded)"
            lines.append(f"  {ids[cid]}{left}{label}{right}")
        for src, rel, dst in edges:
            if rel in HIDDEN_IN_DIAGRAM or src not in ids or dst not in ids:
                continue
            lines.append(f"  {ids[src]} -- {rel} --> {ids[dst]}")
        lines.append("```")
        name = bundle.replace("/", "--")
        header = f"# Grafo · {bundle}\n\n> Gerado por `tools/build_graph.py`. Não edite à mão.\n\n"
        (out / f"{name}.md").write_text(header + "\n".join(lines) + "\n", encoding="utf-8")

    stale = {p.name for p in out.glob("*.md")} - {b.replace("/", "--") + ".md" for b in bundles}
    for name in stale:
        (out / name).unlink()

    print(f"{len(nodes)} nós · {len(edges)} arestas · {len(bundles)} bundles → graph/")


if __name__ == "__main__":
    build()
