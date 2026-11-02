# 03 · Tipos de conceito

A definição executável está em [`schema/ontology.yaml`](../schema/ontology.yaml). Cada tipo tem um template em [`templates/concepts/`](../templates/concepts/).

| Tipo | Pasta | Memória | É… | Envelhece como |
|---|---|---|---|---|
| `Domain` | `index.md` | navegação | porta de entrada do bundle | atualizado a cada conceito novo |
| `Log` | `log.md` | histórico | registro de mudanças | só cresce |
| `Decision` | `decisions/` | semântica | ADR | **imutável**; muda por substituição |
| `BusinessRule` | `rules/` | semântica | regra de negócio | muda com o produto |
| `Term` | `terms/` | semântica | termo da linguagem ubíqua | raramente |
| `Service` | `services/` | semântica | serviço/sistema (interno ou externo) | muda com o código |
| `Runbook` | `runbooks/` | procedimental | como fazer algo recorrente | muda com o processo |
| `Incident` | `incidents/` | episódica | postmortem | não muda; gera lições |
| `Meeting` | `meetings/` | episódica | resumo curto de reunião | **expira**; o valor está no que gerou |

## Decision (ADR)

- Seções obrigatórias: `## Contexto` · `## Decisão` · `## Alternativas rejeitadas` · `## Consequências`
- Recomendada: `## Revisitar quando` — a condição que justificaria rever (evita que "já foi rejeitado" vire dogma).
- `status`: `candidate` (proposta) → `active` (aceita) → `superseded` (quando outra a substitui) ou `deprecated`.
- **Nunca edite o conteúdo de uma decisão `active`.** Para mudar, crie uma nova com `supersedes:` e marque a antiga como `superseded`.
- Critério para virar ADR: decisão difícil de reverter, ou que já gerou discussão repetida. Não crie ADR para detalhe de implementação.

## BusinessRule

- Seções: `## Regra` (uma frase verificável) · `## Motivo`
- Recomendado: `implements` vindo do `Service` que a aplica, e fonte `code` apontando o símbolo.

## Term

- Seções: `## Definição` · `## Exemplo` · `## Não confundir com`
- Um termo por arquivo. Sinônimos vão em `tags`.

## Service

- Campo obrigatório: `resource` (URL do repo, ou do sistema externo).
- Seções: `## Responsabilidade` · `## Interfaces` (entradas/saídas) · `## Armadilhas`
- Serviços externos (adquirente, banco central, SaaS) também são `Service`, com `tags: [external]`.
- O esqueleto (`resource`, `owner`, `dependsOn`) deve ser **gerado do código** quando possível; o texto é curado.

## Runbook

- Seções: `## Quando usar` · `## Passos` · `## Como verificar`
- Se existir uma skill executável, aponte para ela em `sources` (`kind: url` ou `doc`).

## Incident

- Seções: `## Resumo` · `## Impacto` · `## Causa` · `## Lições`
- Cada lição relevante vira um conceito próprio (`BusinessRule`, `Runbook`, `Decision`) ligado por `produced`.

## Meeting

- `expires` obrigatório (padrão: 90 dias).
- Corpo curto: bullets com o que foi decidido/definido, cada um apontando para o conceito gerado.
- Campo recomendado: `participants` (times, não pessoas).
- **Nunca** a transcrição. Ver [02 · O que não entra](02-formato.md#o-que-não-entra-no-bundle).

## Adicionar um tipo novo

PR alterando `schema/ontology.yaml`, esta página e `templates/concepts/`, revisado pelos donos de `org/`. Antes, confira se um tipo existente com `tags` não resolve.
