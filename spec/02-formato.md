# 02 · Formato dos conceitos (OKF + extensões)

Todo conhecimento compartilhado é um **conceito**: um arquivo Markdown com frontmatter YAML, uma ideia por arquivo. Isso é [OKF v0.1](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) válido; os campos extras abaixo são extensões nossas, permitidas pelo OKF.

## Identidade

- **O caminho do arquivo a partir da raiz do repo é o ID do conceito** (regra do OKF). Ex.: `domains/payments/decisions/0057-pix-parcelado.md`.
- Nomes de arquivo: `kebab-case`, sem acentos. ADRs e incidentes com prefixo ordenável (`0057-…`, `2026-10-14-…`).
- Mover ou renomear um conceito quebra referências: o validador acusa; corrija os links no mesmo PR.

## Frontmatter

```yaml
---
# ── Campos OKF ───────────────────────────────────────────────
type: Decision                      # OBRIGATÓRIO (OKF). Ver spec/03-tipos.md
title: "ADR-0057: Pix parcelado com mínimo de R$ 100"
description: Uma frase que responde "do que se trata?".
tags: [pix, parcelamento]
timestamp: 2026-10-30               # última alteração relevante do conteúdo
resource: https://github.com/org/payments-api   # (opcional) o recurso real descrito

# ── Extensões agents-memory ─────────────────────────────────
owner: time-pagamentos              # time dono (não pessoa)
status: active                      # candidate | active | superseded | deprecated
trust: canonical                    # canonical | inferred
expires: 2026-12-01                 # obrigatório se trust=inferred e em Meeting
last_verified: 2026-11-01           # última vez que alguém/algo confirmou contra a fonte
sources:                            # de onde veio; obrigatório (exceto Domain e Log)
  - kind: meeting                   # code | pr | adr | meeting | doc | ticket | url | incident
    ref: domains/payments/meetings/2026-w44-produto.md
    quote: "abaixo de 100 reais o custo da operação não fecha"
  - kind: code
    ref: payments-api:src/rules/installments.ts#validateMinimumAmount
relations:                          # arestas tipadas; alvos são IDs (caminhos)
  partOf: [domains/payments/index.md]
  supersedes: [domains/payments/decisions/0031-parcelamento-proprio.md]
  decidesAbout: [domains/payments/rules/pix-parcelado-minimo.md]
---
```

### Campos obrigatórios por tipo

| Campo | Domain | Log | Demais tipos |
|---|---|---|---|
| `type`, `title` | ✅ | ✅ | ✅ |
| `description`, `owner`, `timestamp` | ✅ | — | ✅ |
| `status`, `trust`, `sources` | — | — | ✅ |
| `expires` | — | — | se `trust: inferred`; sempre em `Meeting` |

Campos obrigatórios específicos de cada tipo (ex.: `resource` em `Service`) estão em [03-tipos.md](03-tipos.md) e em [`schema/ontology.yaml`](../schema/ontology.yaml).

### `sources`

Cada fonte é `{kind, ref, quote?}`.

| `kind` | Formato de `ref` | Exemplo |
|---|---|---|
| `code` | `<repo>:<caminho>#<símbolo>` (prefira símbolo a linha) | `payments-api:src/routes/charge.ts#createCharge` |
| `pr` | URL do PR | `https://github.com/org/payments-api/pull/812` |
| `adr`, `meeting`, `incident`, `doc` | ID de conceito neste repo, ou URL | `domains/payments/meetings/2026-w44-produto.md` |
| `ticket` | Chave ou URL | `PAY-812` |
| `url` | URL | — |

`quote` é um trecho **literal** da fonte. É obrigatório quando a fonte é humana (reunião, PR, documento) e a afirmação é uma decisão ou regra — é o que permite verificar sem reler a fonte inteira.

## Relações

As relações vão em `relations`, como `nome: [lista de IDs]`. O vocabulário é fechado e definido em [`schema/ontology.yaml`](../schema/ontology.yaml); o validador recusa nomes ou pares de tipo fora dele.

| Relação | De → Para | Origem | Pergunta que responde |
|---|---|---|---|
| `partOf` | qualquer → `Domain` | Backstage | O que existe neste domínio? |
| `dependsOn` | `Service` → `Service` | Backstage | Se X cair, o que quebra? |
| `implements` | `Service` → `BusinessRule` | nossa | Onde essa regra está no código? |
| `decidesAbout` | `Decision` → `Service`, `BusinessRule`, `Runbook`, `Term` | nossa | Por que é assim? |
| `supersedes` | `Decision` → `Decision` | nossa | Isso ainda vale? |
| `usesTerm` | qualquer → `Term` | nossa | O que esse termo significa aqui? |
| `causedBy` | `Incident` → `Service`, `Decision` | nossa | Isso já deu problema? |
| `produced` | `Incident`, `Meeting` → qualquer | nossa | O que aprendemos/decidimos? |
| `relatesTo` | qualquer → qualquer | nossa | Use só quando nenhuma outra serve |

Regras:
- Declare a relação **em um lado só** (no conceito de origem). O inverso (`hasPart`, `dependencyOf`, `supersededBy`, "citado por") é **gerado** no grafo.
- Para adicionar uma relação nova: PR em `schema/ontology.yaml` + esta tabela, revisado pelos donos de `org/`.

## Corpo

- Markdown livre, com as **seções obrigatórias do tipo** (`## Contexto`, `## Decisão`…).
- Links entre conceitos no corpo usam **links Markdown relativos** (`[ADR-0042](../decisions/0042-idempotencia.md)`) — renderizam no GitHub e o agente segue com uma leitura de arquivo. O validador checa que resolvem.
- Limite: **~400 palavras** (o validador avisa acima disso). Passou, quebre em conceitos menores.
- Não use `[[wikilinks]]`.

## Bundles

Um **bundle** é uma pasta com um domínio (ou `org/`). Estrutura:

```
domains/<dominio>/
├── index.md          # type: Domain  — porta de entrada (OKF reserva este nome)
├── log.md            # type: Log     — histórico de mudanças (OKF reserva este nome)
├── decisions/        # Decision
├── rules/            # BusinessRule
├── terms/            # Term
├── services/         # Service
├── runbooks/         # Runbook
├── incidents/        # Incident
├── meetings/         # Meeting (resumos curtos, expiram)
└── evals/            # perguntas com resposta-ouro (spec/05-evals.md)
```

- **Por domínio, não por time.** Times mudam; o campo `owner` diz quem cuida hoje.
- **`org/`** é o bundle da empresa: padrões transversais, termos compartilhados, decisões que afetam todos.
- **Cada domínio tem sua linguagem.** Se "cliente" significa coisas diferentes em dois domínios, cada um tem seu `Term`; o de `org/` só existe se o significado for realmente comum.
- **Criar um domínio**: copie a estrutura de [`examples/payments/`](../examples/payments/), ajuste `index.md`, registre em `log.md`.

### `index.md` (type: Domain)

Porta de entrada do bundle. É o que o agente lê primeiro ao chegar no domínio. Seções:
`## O que é` · `## Serviços` · `## Decisões vigentes` · `## Regras de negócio` · `## Termos-chave` · `## Runbooks` · `## Repos`.
Liste com links; mantenha abaixo de ~60 linhas.

### `log.md` (type: Log)

Histórico de mudanças do bundle, mais recente primeiro, uma linha por mudança:

```markdown
- 2026-10-30 · added · decisions/0057-pix-parcelado.md · time-pagamentos · reunião de produto W44
- 2026-10-30 · superseded · decisions/0031-parcelamento-proprio.md · time-pagamentos · substituído pelo ADR-0057
```

Ações: `added` · `updated` · `superseded` · `deprecated` · `removed` · `verified`.
Serve para o agente responder "o que mudou neste domínio?" sem ler o git.

## O que NÃO entra no bundle

| Não entra | Onde fica |
|---|---|
| Transcrições de reunião, logs brutos | Fora do repo, retenção curta (ver [07](07-governanca.md)) |
| Instruções de um repo específico | `AGENTS.md` do repo |
| Procedimentos executáveis por agente (`SKILL.md`) | Plugin/skills do time; o `Runbook` aponta para a skill |
| Preferências pessoais | `~/.claude/CLAUDE.md` ou `CLAUDE.local.md` |
| Segredos, dados pessoais | Nunca |
