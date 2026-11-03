#!/usr/bin/env python3
"""Navegação guiada pela memória: busca, descida pela árvore e percurso no grafo, lendo pouco de cada vez.

Uso (da raiz do repo):
  python tools/memory.py domains
  python tools/memory.py tree [pasta] [--depth 1]
  python tools/memory.py search "termo ..." [--domain d] [--type T]
  python tools/memory.py read <id> [--summary]
  python tools/memory.py neighbors <id> [--depth 1]
  python tools/memory.py history <id>
  python tools/memory.py queue [--domain d] [--days 14]
Opções comuns: --limit N (padrão 20), --all (inclui os bundles de exemplo).

<id> aceita a chave (knowledge/domains/x/rules/y), o ID OKF (/domains/x/rules/y), o caminho do
arquivo ou um final único (rules/y). Só lê. São as mesmas operações do MCP previsto em spec/06.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import unicodedata
from collections import defaultdict, deque

from memlib import ROOT, as_datetime, concepts_by_key, edges, load_docs, load_ontology, trust_tier

STOPWORDS = set("a o as os de da do das dos e em no na nos nas um uma para por com que se ao".split())
TRUST = {"human-reviewed": "revisado por humano", "machine-confirmed": "confirmado por máquina",
         "unverified": "não verificado"}
REAL_BUNDLE = "knowledge"


def iso(value) -> str:
    return value.strftime("%Y-%m-%dT%H:%M:%SZ") if isinstance(value, dt.datetime) else str(value)


def fold(text: str) -> str:
    """Minúsculas e sem acentos, para busca."""
    return "".join(c for c in unicodedata.normalize("NFKD", str(text).lower()) if not unicodedata.combining(c))


class Memoria:
    def __init__(self, todos: bool):
        onto = load_ontology()
        self.onto = onto
        self.now = dt.datetime.now(dt.timezone.utc)
        self.everything = concepts_by_key(load_docs(onto))
        self.concepts = {k: d for k, d in self.everything.items() if todos or d.bundle == REAL_BUNDLE}
        self.out, self.inc = defaultdict(list), defaultdict(list)
        for s, r, t, txt in edges(self.concepts):
            self.out[s].append((r, t, txt))
            self.inc[t].append((r, s, txt))

    @staticmethod
    def area(key: str) -> str:
        """Valor aceito por --domain: o nome do domínio, "org" ou o bundle de exemplo."""
        parts = key.split("/")
        if parts[0] == REAL_BUNDLE:
            return parts[2] if parts[1] == "domains" and len(parts) > 3 else parts[1]
        return "/".join(parts[:2])

    def check_domain(self, domain: str | None) -> None:
        known = {self.area(k) for k in self.concepts}
        if domain and domain not in known:
            sys.exit(f"Domínio desconhecido: {domain!r}. Valores aceitos em --domain: {', '.join(sorted(known))}"
                     + (" (exemplos só com --all)" if any(self.area(k) == domain for k in self.everything) else ""))

    def flags(self, d) -> str:
        fm = d.fm
        parts = [TRUST[trust_tier(fm)]]
        if fm.get("status", "stable") != "stable":
            parts.append(fm["status"])
        stale = as_datetime(fm.get("stale_after"))
        if stale and stale <= self.now:
            parts.append(f"vencido desde {stale:%Y-%m-%d}")
        return ", ".join(parts)

    def line(self, key: str, desc: bool = False) -> str:
        d = self.concepts[key]
        s = f"{key} · {d.type} · {d.fm.get('title') or d.id} · {self.flags(d)}"
        if desc and d.fm.get("description"):
            s += f"\n    {d.fm['description']}"
        return s

    def resolve(self, ref: str) -> str:
        ref = ref.strip().removesuffix(".md").rstrip("/")
        for cand in (ref, REAL_BUNDLE + ref if ref.startswith("/") else None):
            if cand in self.concepts:
                return cand
        hits = [k for k in self.concepts if k.endswith("/" + ref.lstrip("/"))]
        if not hits:   # começo do nome do arquivo, ex.: "0057" ou "0057-pix"
            hits = [k for k in self.concepts if k.rsplit("/", 1)[-1].startswith(ref.rsplit("/", 1)[-1])
                    and ("/" not in ref or ("/" + ref.rsplit("/", 1)[0] + "/") in k)]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            if self.everything is not self.concepts and len(self.everything) > len(self.concepts):
                extra = [k for k in self.everything if k not in self.concepts and k.rsplit("/", 1)[-1].startswith(ref.rsplit("/", 1)[-1])]
                if extra:
                    sys.exit(f"{ref!r} só existe nos exemplos ({', '.join(sorted(extra))}). Use --all.")
            sys.exit(f"Nenhum conceito para {ref!r}. Use `search` ou `tree`.")
        sys.exit(f"{ref!r} é ambíguo:\n" + "\n".join("  " + h for h in sorted(hits)))


def limited(items: list[str], limite: int) -> None:
    for s in items[:limite]:
        print(s)
    if len(items) > limite:
        print(f"… e mais {len(items) - limite} (use --limit)")


def cmd_domains(m: Memoria, a) -> None:
    counts = defaultdict(int)
    for k in m.concepts:
        counts[m.area(k)] += 1
    base = ROOT / REAL_BUNDLE / "domains"
    for p in sorted(base.iterdir()) if base.exists() else []:
        if p.is_dir():
            counts.setdefault(p.name, 0)
    for area, n in sorted(counts.items()):
        path = area if "/" in area else (f"{REAL_BUNDLE}/{area}" if area == "org" else f"{REAL_BUNDLE}/domains/{area}")
        print(f"{area} · {n} conceito(s) · pasta {path}/")
    print("\nPróximo passo: `tree <pasta>` para descer, ou `search \"termos\" --domain <nome>`.")


def cmd_tree(m: Memoria, a) -> None:
    prefix = (a.path or REAL_BUNDLE).strip("/").removesuffix(".md")
    if prefix in m.concepts:
        sys.exit(f"{prefix} é um conceito. Use `read {prefix}`.")
    keys = sorted(k for k in m.concepts if k.startswith(prefix + "/"))
    if not keys:
        sys.exit(f"Nada em {prefix}/. Use `domains`.")
    index = ROOT / prefix / "index.md"
    print(f"{prefix}/" + (f"  (índice curado: {prefix}/index.md)" if index.exists() else ""))
    depth = len(prefix.split("/"))
    rows = []

    def walk(path: list[str], level: int) -> None:
        here = [k for k in keys if k.split("/")[depth:depth + len(path)] == path]
        pad = "  " * (len(path) + 1)
        subfolders = sorted({k.split("/")[depth + len(path)] for k in here if len(k.split("/")) > depth + len(path) + 1})
        for f in subfolders:
            n = sum(1 for k in here if k.split("/")[depth + len(path)] == f and len(k.split("/")) > depth + len(path) + 1)
            rows.append(f"{pad}{f}/ · {n} conceito(s)")
            if level < a.depth:
                walk(path + [f], level + 1)
        for k in here:
            if len(k.split("/")) == depth + len(path) + 1:
                rows.append(pad + m.line(k, desc=True).replace("\n", "\n" + pad))

    walk([], 1)
    limited(rows, a.limit * 2)
    if any(r.rstrip().endswith("conceito(s)") for r in rows):
        print("\nPróximo passo: `tree <pasta>` ou `--depth 2` para ver os conceitos; `read <id>` para abrir um.")


def cmd_search(m: Memoria, a) -> None:
    m.check_domain(a.domain)
    terms = [t for t in (fold(t) for t in a.terms.split()) if t and t not in STOPWORDS]
    weights = (("title", 5), ("tags", 4), ("description", 3))
    scored = []
    for k, d in m.concepts.items():
        if a.domain and m.area(k) not in (a.domain, "org"):   # org vale para todos os domínios
            continue
        if a.type and fold(d.type) != fold(a.type):
            continue
        fields = {f: fold(" ".join(d.fm.get(f)) if isinstance(d.fm.get(f), list) else d.fm.get(f) or "")
                  for f, _ in weights}
        body = fold(d.body)
        score, hit = 0, 0
        for t in terms:
            s = sum(w for f, w in weights if t in fields[f]) + (2 if t in fold(k) else 0) + (1 if t in body else 0)
            score, hit = score + s, hit + (1 if s else 0)
        if score:
            snippet = next((ln.strip() for ln in d.body.splitlines()
                            if ln.strip() and any(t in fold(ln) for t in terms)), "")
            scored.append((-hit, -score, k, snippet[:140]))
    if not scored:
        print("Nada encontrado. Tente sinônimos, ou `tree` para navegar.")
        return
    rows = []
    for neg_hit, _, k, snip in sorted(scored):
        rows.append(f"[{-neg_hit}/{len(terms)} termos] " + m.line(k, desc=True) + (f"\n    … {snip}" if snip else ""))
    limited(rows, a.limit)
    print("\nPróximo passo: `read <id>` no mais promissor.")


def cmd_read(m: Memoria, a) -> None:
    k = m.resolve(a.id)
    d = m.concepts[k]
    fm = d.fm
    print(f"# {fm.get('title') or d.id}")
    print(f"id: {k} · tipo: {d.type} · confiança: {m.flags(d)}")
    if fm.get("description"):
        print(f"descrição: {fm['description']}")
    gen = fm.get("generated")
    if isinstance(gen, dict):
        print(f"escrito por: {gen.get('by')} em {iso(gen.get('at'))}")
    for v in fm.get("verified") if isinstance(fm.get("verified"), list) else [fm["verified"]] if fm.get("verified") else []:
        print(f"verificado por: {v.get('by')} em {iso(v.get('at'))}")
    if fm.get("stale_after"):
        print(f"stale_after: {iso(fm['stale_after'])}")
    for s in fm.get("sources") or []:
        if isinstance(s, dict):
            print(f"fonte [{s.get('id')}]: " + (f"{s['title']} → " if s.get("title") else "") + str(s.get("resource")))
    if not a.summary:
        print("\n" + d.body.strip())
    print()
    print_edges(m, k)


def print_edges(m: Memoria, k: str) -> None:
    out, inc = m.out.get(k, []), m.inc.get(k, [])
    if out:
        print("Liga para:")
        for r, t, txt in out:
            print(f"  → {m.line(t)}\n      {'fonte' if r == 'source' else txt}")
    if inc:
        print("Ligado por:")
        for r, s, txt in inc:
            print(f"  ← {m.line(s)}\n      {'usa como fonte' if r == 'source' else txt}")
    if not out and not inc:
        print("Sem ligações com outros conceitos.")


def cmd_neighbors(m: Memoria, a) -> None:
    start = m.resolve(a.id)
    seen, queue, rows = {start}, deque([(start, 0)]), []
    while queue:
        k, dist = queue.popleft()
        if dist == a.depth:
            continue
        for arrow, items in (("→", m.out.get(k, [])), ("←", m.inc.get(k, []))):
            for r, other, txt in items:
                if other in seen:
                    continue
                seen.add(other)
                how = ("fonte" if arrow == "→" else "usa como fonte") if r == "source" else txt
                rows.append(f"{'  ' * dist}{arrow} {m.line(other)}\n{'  ' * dist}    {how}")
                queue.append((other, dist + 1))
    print(m.line(start))
    limited(rows, a.limit) if rows else print("Sem vizinhos.")


def cmd_history(m: Memoria, a) -> None:
    start = m.resolve(a.id)
    chain, queue = {start}, deque([start])
    while queue:
        k = queue.popleft()
        for items in (m.out.get(k, []), m.inc.get(k, [])):
            for r, other, txt in items:
                if r == "link" and "substitu" in fold(txt) and m.concepts[other].type == "Decision" and other not in chain:
                    chain.add(other)
                    queue.append(other)
    def when(k):
        gen = m.concepts[k].fm.get("generated")
        at = as_datetime(gen.get("at")) if isinstance(gen, dict) else None
        return (at or dt.datetime.min.replace(tzinfo=dt.timezone.utc), k)

    for k in sorted(chain, key=when):
        at = when(k)[0]
        current = m.concepts[k].fm.get("status", "stable") != "deprecated"
        print(f"{at:%Y-%m-%d} · " + m.line(k) + ("  ← vigente" if current else ""))
        for r, other, txt in m.out.get(k, []):
            if other in chain and "substitu" in fold(txt):
                print(f"    {txt}")


def cmd_queue(m: Memoria, a) -> None:
    m.check_domain(a.domain)
    soon = m.now + dt.timedelta(days=a.days)
    risky = set(m.onto["human_review_tags"])
    rows = []
    for k, d in m.concepts.items():
        if a.domain and m.area(k) != a.domain:
            continue
        fm, status = d.fm, d.fm.get("status", "stable")
        trust, stale = trust_tier(fm), as_datetime(fm.get("stale_after"))
        why = []
        if stale and stale <= m.now:
            why.append(f"venceu em {stale:%Y-%m-%d}")
        elif stale and stale <= soon:
            why.append(f"vence em {stale:%Y-%m-%d}")
        if status == "draft":
            why.append("draft")
        if trust == "unverified" and status != "deprecated":
            why.append("não verificado")
        human = m.onto["types"].get(d.type, {}).get("human_review") or (set(fm.get("tags") or []) & risky)
        if human and trust != "human-reviewed" and status != "deprecated":
            why.append("pede humano para sair de draft" if status == "draft" else "pede humano")
        if why:
            rows.append((0 if stale and stale <= m.now else 1, k, why))
    if not rows:
        print("Fila vazia.")
        return
    limited([f"{m.line(k)}\n    motivo: {', '.join(why)}" for _, k, why in sorted(rows)], a.limit)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--limit", type=int, default=20)
    common.add_argument("--all", action="store_true", help="inclui os bundles de exemplo")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("domains", parents=[common])
    p = sub.add_parser("tree", parents=[common]); p.add_argument("path", nargs="?"); p.add_argument("--depth", type=int, default=1)
    p = sub.add_parser("search", parents=[common]); p.add_argument("terms"); p.add_argument("--domain"); p.add_argument("--type")
    p = sub.add_parser("read", parents=[common]); p.add_argument("id"); p.add_argument("--summary", action="store_true")
    p = sub.add_parser("neighbors", parents=[common]); p.add_argument("id"); p.add_argument("--depth", type=int, default=1, choices=[1, 2, 3])
    p = sub.add_parser("history", parents=[common]); p.add_argument("id")
    p = sub.add_parser("queue", parents=[common]); p.add_argument("--domain"); p.add_argument("--days", type=int, default=14)
    a = ap.parse_args()
    m = Memoria(a.all)
    globals()[f"cmd_{a.cmd}"](m, a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
