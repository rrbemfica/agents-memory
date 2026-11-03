# 03 · Tipos de conceito

A OKF não tem taxonomia fixa de tipos: cada produtor define os seus (OKF §4.1). Estes são os nossos. A definição está em [`schema/ontology.yaml`](../schema/ontology.yaml), e cada tipo tem um template em [`templates/concepts/`](../templates/concepts/).

**Tudo nesta página é recomendação:** o validador avisa quando algo não é seguido, mas não bloqueia. Um conceito com outro `type` continua sendo OKF válido.

| `type` | Pasta | Memória | É… | Envelhece como |
|---|---|---|---|---|
| `Decision` | `decisions/` | semântica | ADR | **imutável**; muda por substituição |
| `Business Rule` | `rules/` | semântica | regra de negócio | muda com o produto |
| `Term` | `terms/` | semântica | termo da linguagem ubíqua | raramente |
| `Service` | `services/` | semântica | serviço ou sistema (interno ou externo) | muda com o código |
| `Runbook` | `runbooks/` | procedimental | como fazer algo recorrente | muda com o processo |
| `Incident` | `incidents/` | episódica | postmortem | não muda; gera lições |
| `Meeting` | `meetings/` | episódica | resumo curto de reunião | **fica velho rápido**; o valor está no que gerou |

`index.md` e `log.md` não são tipos: são arquivos reservados da OKF ([02](02-formato.md#indexmd-okf-8)).

## Decision (ADR)

- Seções recomendadas: `# Contexto` · `# Decisão` · `# Alternativas rejeitadas` · `# Consequências`.
- Recomendada: `# Revisitar quando`, a condição que justificaria rever. Evita que "já foi rejeitado" vire dogma.
- Recomendado: ao menos uma nota de rodapé com o trecho literal da fonte entre aspas.
- **Para ser `stable`, recomendamos humano:** um ator `human:` em `generated.by` ou em `verified`. Agentes podem propor decisões em `draft`.
- `status`: `draft` (proposta) → `stable` (aceita) → `deprecated` (substituída ou abandonada).
- **Não edite o conteúdo de uma decisão `stable`.** Para mudar, crie uma nova com "Substitui [ADR-…]" em `# Relacionados`, marque a antiga como `deprecated` e acrescente nela "Substituída por […]".
- Vira ADR quando a decisão é difícil de reverter ou já gerou discussão repetida. Detalhe de implementação não vira ADR.

## Business Rule

- Seções: `# Regra` (uma frase verificável) · `# Motivo`.
- Recomendado: o `Service` que aplica a regra diz "Implementa […]" em `# Relacionados`, e uma fonte aponta o símbolo no código.

## Term

- Seções: `# Definição` · `# Exemplo` · `# Não confundir com`.
- Um termo por arquivo. Sinônimos vão em `tags`.

## Service

- Campo recomendado: `resource` (URL do repo ou do sistema externo).
- Seções: `# Responsabilidade` · `# Interfaces` (entradas e saídas) · `# Armadilhas`.
- Serviços externos (adquirente, banco central, SaaS) também são `Service`, com `tags: [external]`.
- O esqueleto (`resource` e os "Depende de") deve ser **gerado do código** quando possível; o texto é curado.

## Runbook

- Seções: `# Quando usar` · `# Passos` · `# Como verificar`.
- Se existir uma skill executável, ela entra em `sources`.

## Incident

- Seções: `# Resumo` · `# Impacto` · `# Causa` · `# Lições`.
- Cada lição relevante vira um conceito próprio (`Business Rule`, `Runbook`, `Decision`), linkado na seção `# Lições`.

## Meeting

- `stale_after` recomendado (padrão: 90 dias depois da reunião).
- Corpo curto: bullets com o que foi decidido ou definido, cada um apontando para o conceito gerado.
- Primeiro bullet: `Participantes:`, com times, não pessoas.
- **Nunca** a transcrição.

## Tipos da OKF que podemos adotar depois

- **`Attested Computation`** (OKF §10): uma forma sancionada de calcular um número, com um verificador determinístico. Útil quando o domínio tiver métricas oficiais (receita, conversão) que agentes precisem calcular sem improvisar a query.

## Adicionar um tipo novo

PR alterando `schema/ontology.yaml`, esta página e `templates/concepts/`, revisado pelos donos de `knowledge/org/`. Antes, confira se um tipo existente com `tags` não resolve.
