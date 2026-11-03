#!/usr/bin/env python3
"""Lista a fila de revisão de um repo agents-memory: drafts, não verificados e stale_after vencendo.

Uso: python fila.py <repo-agents-memory> [--dominio <nome>] [--dias 14] [--todos]
Só lê. Usa tools/memlib.py do próprio repo, para seguir as mesmas regras do validador.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("--dominio", help="só knowledge/domains/<dominio>/")
    ap.add_argument("--dias", type=int, default=14, help="janela para stale_after que vai vencer")
    ap.add_argument("--todos", action="store_true", help="inclui bundles de exemplo (padrão: só knowledge/)")
    args = ap.parse_args()

    tools = args.repo.resolve() / "tools"
    if not (tools / "memlib.py").exists():
        print(f"não achei tools/memlib.py em {args.repo}; é o repo agents-memory?", file=sys.stderr)
        return 2
    sys.path.insert(0, str(tools))
    from memlib import ROOT, as_datetime, concepts_by_key, load_docs, load_ontology, trust_tier

    onto = load_ontology()
    now = dt.datetime.now(dt.timezone.utc)
    soon = now + dt.timedelta(days=args.dias)
    prefix = f"/domains/{args.dominio}/" if args.dominio else ""
    risky_tags = set(onto["human_review_tags"])

    rows = []
    for d in concepts_by_key(load_docs(onto)).values():
        if d.bundle != "knowledge" and not args.todos:
            continue
        if prefix and not (d.bundle == "knowledge" and d.id.startswith(prefix)):
            continue
        fm = d.fm
        status = fm.get("status", "stable")
        trust = trust_tier(fm)
        stale = as_datetime(fm.get("stale_after"))
        motivos = []
        if stale and stale <= now:
            motivos.append(f"venceu em {stale:%Y-%m-%d}")
        elif stale and stale <= soon:
            motivos.append(f"vence em {stale:%Y-%m-%d}")
        if status == "draft":
            motivos.append("draft")
        if trust == "unverified" and status != "deprecated":
            motivos.append("não verificado")
        human = onto["types"].get(d.type, {}).get("human_review") or (set(fm.get("tags") or []) & risky_tags)
        if human and trust != "human-reviewed" and status != "deprecated":
            motivos.append("pede humano para sair de draft" if status == "draft" else "pede humano")
        if motivos:
            rows.append((0 if stale and stale <= now else 1, d.path.relative_to(ROOT).as_posix(), d.type, status, trust, motivos))

    if not rows:
        print("Fila vazia.")
        return 0
    print("| Conceito | Tipo | Status | Confiança | Motivo |")
    print("|---|---|---|---|---|")
    for _, path, t, status, trust, motivos in sorted(rows):
        print(f"| {path} | {t} | {status} | {trust} | {', '.join(motivos)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
