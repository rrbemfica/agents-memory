# agents-memory

A memória compartilhada do time, feita para ser lida e escrita por **pessoas e agentes** (Claude Code, Codex, Cursor, Copilot…).

```
┌──────────────────────────────┐        ┌───────────────────────────────────┐
│  Repos de projeto            │        │  agents-memory (este repo)        │
│                              │        │                                   │
│  AGENTS.md  ← instruções     │ ─────► │  org/            bundle da empresa│
│  (comandos, armadilhas,      │ aponta │  domains/<nome>/ bundle por domínio│
│   limites)                   │  para  │     index.md  log.md  conceitos   │
│  lido automaticamente        │        │     evals/                        │
└──────────────────────────────┘        └───────────────────────────────────┘
                                              │ gerado no CI
                                              ▼
                                        graph/  (grafo, Mermaid, backlinks)
```

- **Repos de projeto** usam [`AGENTS.md`](spec/01-agents-md.md): instruções curtas e locais, carregadas automaticamente pelos agentes.
- **Conhecimento do time e do domínio** (decisões, regras de negócio, termos, serviços, runbooks, incidentes) vive aqui, em bundles no formato [**Open Knowledge Format (OKF)**](spec/02-formato.md) com extensões nossas para relações tipadas, confiança e fonte.
- **Qualidade é medida**, não presumida: toda nota cita sua fonte e cada domínio tem [evals](spec/05-evals.md) que medem acurácia.

## Por onde começar

| Quero… | Leia |
|---|---|
| Entender o modelo | [spec/00-visao-geral.md](spec/00-visao-geral.md) |
| Escrever o AGENTS.md de um repo | [spec/01-agents-md.md](spec/01-agents-md.md) · [template](templates/AGENTS.md) |
| Criar um conceito (ADR, termo, regra…) | [spec/03-tipos.md](spec/03-tipos.md) · [templates/concepts/](templates/concepts/) |
| Criar um domínio novo | [spec/02-formato.md](spec/02-formato.md#bundles) · copie [examples/payments/](examples/payments/) |
| Saber como uma nota entra e sai | [spec/04-ciclo-de-vida.md](spec/04-ciclo-de-vida.md) |
| Medir se a memória funciona | [spec/05-evals.md](spec/05-evals.md) |
| Ver um domínio completo | [examples/payments/index.md](examples/payments/index.md) |

## Comandos

```bash
pip install -r tools/requirements.txt
python tools/validate.py        # valida frontmatter, tipos, relações, links, evals e segredos
python tools/build_graph.py     # gera graph/ (graph.json, backlinks.json, Mermaid por domínio)
```

O CI (`.github/workflows/memory-ci.yml`) roda os dois em todo PR e falha se o grafo commitado estiver desatualizado.

## Status

| Peça | Status |
|---|---|
| Especificação (`spec/`) | ✅ v0.1 |
| Templates e domínio de exemplo | ✅ |
| Validador e gerador de grafo + CI | ✅ |
| Servidor MCP de leitura (`search`, `get`, `neighbors`, `impact`) | 📐 especificado em [06](spec/06-grafo-e-acesso.md), não implementado |
| Runner de evals com/sem memória | 📐 especificado em [05](spec/05-evals.md), não implementado |
| Gardener noturno (verificação de fontes, expiração) | 📐 especificado em [04](spec/04-ciclo-de-vida.md), parcial (expiração é checada no validador) |
