# agents-memory

A memória compartilhada do time, feita para ser lida e escrita por **pessoas e agentes** (Claude Code, Codex, Cursor, Copilot…).

```
┌──────────────────────────────┐        ┌───────────────────────────────────┐
│  Repos de projeto            │        │  agents-memory (este repo)        │
│                              │        │                                   │
│  AGENTS.md  ← instruções     │ ─────► │  knowledge/  bundle OKF v0.2      │
│  (comandos, armadilhas,      │ aponta │    org/            transversal    │
│   limites)                   │  para  │    domains/<nome>/ por domínio    │
│  lido automaticamente        │        │     evals/                        │
└──────────────────────────────┘        └───────────────────────────────────┘
                                              │ gerado sob demanda (não versionado)
                                              ▼
                                        graph/  (grafo, Mermaid, backlinks)
```

- **Repos de projeto** usam [`AGENTS.md`](spec/01-agents-md.md): instruções curtas e locais, carregadas automaticamente pelos agentes.
- **Conhecimento do time e do domínio** (decisões, regras de negócio, termos, serviços, runbooks, incidentes) vive aqui, no bundle `knowledge/`, no formato [**Open Knowledge Format (OKF) v0.2**](spec/02-format.md). Só campos do padrão, sem extensões: origem, confiança e frescor usam `sources`, `generated`, `verified`, `status` e `stale_after`; o dono de cada pasta fica no [`CODEOWNERS`](CODEOWNERS).
- **Qualidade é medida**, não presumida: toda nota cita sua fonte, e domínios podem ter [evals](spec/05-evals.md) que medem acurácia (camada nossa, recomendada; o runner ainda não existe).

## Por onde começar

| Quero… | Leia |
|---|---|
| Entender o modelo | [spec/00-overview.md](spec/00-overview.md) |
| Escrever o AGENTS.md de um repo | [spec/01-agents-md.md](spec/01-agents-md.md) · [template](templates/AGENTS.md) |
| Criar um conceito (ADR, termo, regra…) | [spec/03-types.md](spec/03-types.md) · [templates/concepts/](templates/concepts/) |
| Criar um domínio novo | [spec/02-format.md](spec/02-format.md#bundles) · copie [examples/payments/](examples/payments/) |
| Saber como uma nota entra e sai | [spec/04-lifecycle.md](spec/04-lifecycle.md) |
| Medir se a memória funciona | [spec/05-evals.md](spec/05-evals.md) |
| Usar no GitLab | [spec/09-forges.md](spec/09-forges.md) |
| Usar a skill (consultar, registrar, revisar, AGENTS.md) | [spec/10-skills.md](spec/10-skills.md) |
| Ver um domínio completo | [examples/payments/index.md](examples/payments/index.md) |

## Skill

A skill [`agent-memory-skill`](spec/10-skills.md) operacionaliza o padrão: consultar, registrar, fechar a sessão, revisar, criar domínio e escrever o `AGENTS.md`. Segue o padrão aberto Agent Skills. No Claude Code:

```
/plugin install agents-memory --marketplace rrbemfica/agents-memory
```

## Comandos

```bash
pip install -r tools/requirements.txt
python tools/validate.py        # erro: viola a OKF ou vaza segredo · aviso: nossas recomendações
python tools/build_graph.py     # opcional: gera graph/ localmente (não é commitado)
python tools/memory.py search "estorno" --all   # navegar: domains, tree, search, read, neighbors, history, queue
```

O CI roda `tools/ci.sh` em todo PR/MR: valida os bundles e publica o grafo como artefato da pipeline (30 dias), sem commit. Funciona no GitHub (`.github/workflows/memory-ci.yml`) e no GitLab (`.gitlab-ci.yml`); ver [spec/09-forges.md](spec/09-forges.md).

## Status

| Peça | Status |
|---|---|
| Especificação (`spec/`) | ✅ v0.3 (OKF v0.2 pura, sem extensões) |
| Templates e domínio de exemplo | ✅ |
| Validador e gerador de grafo + CI | ✅ |
| Skill `agent-memory-skill` (plugin do Claude Code, padrão Agent Skills) | ✅ v0.1 |
| Navegação guiada (`tools/memory.py`: search, tree, read, neighbors, history) | ✅ |
| Servidor MCP de leitura (mesmas operações) | 📐 especificado em [06](spec/06-graph-and-access.md), não implementado |
| Runner de evals com/sem memória | 📐 especificado em [05](spec/05-evals.md), não implementado |
| Gardener noturno (verificação de fontes, expiração) | 📐 especificado em [04](spec/04-lifecycle.md), parcial (`stale_after` é checado no validador) |
