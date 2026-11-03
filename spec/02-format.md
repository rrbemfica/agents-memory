# 02 · Formato (OKF v0.2)

Todo conhecimento compartilhado é um **conceito**: um arquivo Markdown com frontmatter YAML, uma ideia por arquivo, no formato [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). **Não usamos campos próprios**: só os do padrão. O que acrescentamos são **recomendações** de uso (quais campos e seções preencher). O validador só dá erro para o que viola a OKF; nossas recomendações viram aviso. Resumo [no fim desta página](#o-que-é-padrão-e-o-que-é-recomendação-nossa).

## Bundles

Um **bundle** é a unidade de distribuição da OKF. Neste repo:

| Bundle | Conteúdo |
|---|---|
| [`knowledge/`](../knowledge/index.md) | O conhecimento real: `org/` e um diretório por domínio em `domains/` |
| [`examples/payments/`](../examples/payments/index.md) | Bundle de exemplo, fictício, para copiar |

Regra da OKF: **todo `.md` dentro de um bundle que não seja `index.md` ou `log.md` é um conceito e precisa de frontmatter com `type`.** Por isso spec, README e templates ficam **fora** dos bundles.

```
knowledge/                      # raiz do bundle
├── index.md                    # frontmatter só com okf_version: "0.2"
├── log.md
├── org/                        # conhecimento transversal
│   ├── index.md
│   └── decisions/ …
└── domains/
    ├── index.md
    └── <dominio>/
        ├── index.md            # porta de entrada do domínio (sem frontmatter)
        ├── log.md
        ├── decisions/  rules/  terms/  services/
        ├── runbooks/   incidents/  meetings/
        └── evals/              # .yaml, fora da regra de conformidade (não é .md)
```

- **Por domínio, não por time.** Times mudam; o dono de cada pasta fica no [`CODEOWNERS`](../CODEOWNERS), que também pede a revisão dele nos PRs (ver [09](09-forges.md) sobre quando a forja bloqueia).
- **Cada domínio tem sua linguagem.** Se "cliente" significa coisas diferentes em dois domínios, cada um tem seu `Term`. O `org/` só tem os termos realmente comuns.
- **Criar um domínio:** crie `knowledge/domains/<dominio>/index.md` e `log.md` a partir de [`templates/concepts/`](../templates/concepts/), adicione o time no `CODEOWNERS` e liste o domínio em `knowledge/domains/index.md`. A [skill](10-skills.md) faz isso passo a passo. [`examples/payments/`](../examples/payments/) mostra um domínio completo; se copiar conceitos de lá, os IDs de fontes internas mudam (`/decisions/...` vira `/domains/<dominio>/decisions/...`).

## Identidade e links

- **ID do conceito** (OKF §2): o caminho do arquivo dentro do bundle, sem `.md`. Ex.: `/domains/payments/decisions/0057-pix-parcelado`.
- Nomes de arquivo em `kebab-case`, sem acentos. ADRs e incidentes com prefixo ordenável (`0057-…`, `2026-10-14-…`).
- **Links no corpo:** links Markdown normais. Use **links relativos** (`[ADR-0042](../decisions/0042-idempotencia-adquirente.md)`). A OKF recomenda `/` (relativo à raiz do bundle), mas GitHub e GitLab interpretam `/` como raiz do repo e o link quebra na navegação. É o nosso único desvio consciente de uma recomendação da OKF; o validador aceita as duas formas.
- **Não use link relativo que sai do bundle** (`../../CODEOWNERS`): o bundle é a unidade de distribuição da OKF e o link quebra se ele for distribuído sozinho. Para algo fora do bundle, use URL absoluta.
- **IDs em `sources[].resource` internos:** use a forma relativa ao bundle, com `/` (`/domains/payments/terms/estorno`).

## Frontmatter

```yaml
---
type: Decision                                   # OBRIGATÓRIO na OKF
title: "ADR-0057: Pix parcelado com mínimo de R$ 100"
description: Uma frase que responde "do que se trata?".
resource: https://github.com/org/payments-api    # opcional: o recurso real descrito
tags: [pix, parcelamento]
status: stable                                   # draft | stable | deprecated (ausente = stable)
generated: { by: human:joana, at: 2026-10-30T15:00:00Z }   # quem escreveu, quando mudou
verified:                                        # quem confirmou, quando
  - { by: human:tl-pagamentos, at: 2026-10-31T10:00:00Z }
  - { by: process:memory-evals, at: 2026-11-01T06:00:00Z }
stale_after: 2027-04-30T00:00:00Z                # a partir daqui, considere desatualizado
sources:
  - id: reuniao-w44                              # chave para citação por nota de rodapé
    resource: /domains/payments/meetings/2026-w44-produto
    title: Reunião de produto W44
    author: team:produto
    last_modified: 2026-10-30T14:00:00Z
---
```

### Campos

| Campo | OKF v0.2 | Recomendamos? | Notas |
|---|---|---|---|
| `type` | obrigatório | ✅ | Ver [03-types.md](03-types.md) |
| `title`, `description` | recomendados | ✅ | `description` aparece nos índices |
| `resource` | recomendado | só em `Service` | URL do repo ou sistema |
| `tags` | recomendado | — | Em algumas tags recomendamos revisão humana (ver [04](04-lifecycle.md#quando-pedir-revisão-humana)) |
| `status` | opcional | — | `draft` · `stable` · `deprecated` |
| `generated` | opcional | ✅ | `{by, at}`. `by` é um **ator**: `human:<id>`, `process:<id>` ou `<agente>/<versão>` |
| `verified` | opcional | — | Lista de `{by, at}`. Define o **nível de confiança** (abaixo). Um único mapa vale como lista de um item. |
| `stale_after` | opcional | em `Meeting` e em conceito gerado por agente sem `verified` | Data e hora absolutas (ISO 8601 com fuso) |
| `sources` | opcional | ✅ (≥ 1) | A OKF exige `resource` em cada item |

Todas as datas e horas usam ISO 8601 **com fuso** (`2026-10-30T15:00:00Z`), como exige a OKF.

### Níveis de confiança (OKF §5.3)

Derivados de `verified`, não declarados:

| Nível | Regra | Como o agente trata |
|---|---|---|
| **não verificado** | sem `verified` | Pista: confere a fonte antes de agir |
| **confirmado por máquina** | `verified` só por `process:` ou agentes | Usa, verificando quando o risco for relevante |
| **revisado por humano** | algum `verified` por `human:` | Pode seguir como regra |

### `sources` e citação

- `resource` aceita URL, ID de conceito (`/domains/...`) ou um descritor de escopo ("todas as queries do projeto X").
- Código: `resource: https://github.com/org/repo/blob/main/src/x.ts#L10` ou `repo:caminho#símbolo`. Prefira símbolo a linha.
- **Citação por afirmação** (OKF §5.1): nota de rodapé com o `id` da fonte.
  ```markdown
  O mínimo é R$ 100.[^reuniao-w44]

  [^reuniao-w44]: Reunião de produto W44: "abaixo de 100 reais o custo da operação não fecha"
  ```
- **Trecho literal:** quando der, a nota de rodapé traz o trecho exato da fonte entre aspas. Em `Decision` é fortemente recomendado. É o que permite checar a afirmação sem reler a fonte inteira, e o que o jardineiro usa para conferir se a fonte ainda diz o mesmo.

## Relações entre conceitos

Só links Markdown no corpo, como a OKF define. **Não usamos relações tipadas no frontmatter.** O sentido da ligação vai no texto, numa seção `# Relacionados`:

```markdown
# Relacionados
- Depende de [ledger](ledger.md)
- Implementa [Pix parcelado exige valor mínimo de R$ 100](../rules/pix-parcelado-minimo.md)
- Substitui [ADR-0031](0031-parcelamento-proprio.md)
```

| Verbo sugerido | Use quando |
|---|---|
| Depende de | um serviço chama ou precisa de outro |
| Implementa | o serviço aplica uma regra de negócio |
| Decide sobre | a decisão define uma regra, um serviço, um runbook ou um termo |
| Substitui / Substituída por | uma decisão troca outra (escreva nos dois lados) |
| Usa o termo | o conceito depende do significado de um termo |
| Causado por | o incidente veio de um serviço ou de uma decisão |

- Os verbos são convenção de texto, não campo. Qualquer leitor OKF entende, e o [grafo gerado](06-graph-and-access.md) liga os conceitos.
- "Pertence ao domínio" não precisa ser dito: a hierarquia de pastas já diz isso (OKF §3).
- **Quando voltar a ter relações tipadas:** quando uma pergunta como "o que é afetado se X mudar?" for recorrente e os links não derem conta. A mudança entra por ADR.

## Corpo

- Markdown estruturado (OKF §4.2), com as **seções do tipo** como cabeçalhos `#` (`# Contexto`, `# Decisão`…). As seções de cada tipo são recomendação nossa: a OKF não exige nenhuma.
- Não use `[[wikilinks]]` nem uma lista `# Citations` no corpo (a OKF v0.2 substituiu isso por `sources`).

## `index.md` (OKF §8)

- **Sem frontmatter.** A única exceção é o `index.md` da raiz do bundle, que pode ter só `okf_version: "0.2"`.
- O corpo tem seções, cada uma com uma lista de itens `* [Título](link) - descrição`.
- O `index.md` do domínio é a **porta de entrada**: é o que o agente lê primeiro.

```markdown
# Pagamentos

# Decisões vigentes

* [ADR-0057](decisions/0057-pix-parcelado.md) - Pix parcelado com mínimo de R$ 100
```

## `log.md` (OKF §9)

Sem frontmatter. Entradas agrupadas por data, mais recente primeiro, com a ação em negrito:

```markdown
# Log · Pagamentos

## 2026-10-30
* **Criação**: [ADR-0057](decisions/0057-pix-parcelado.md), Pix parcelado com mínimo de R$ 100.
* **Descontinuação**: [ADR-0031](decisions/0031-parcelamento-proprio.md), substituído pelo ADR-0057.
```

Ações usadas: **Criação** · **Atualização** · **Verificação** · **Descontinuação** · **Remoção**.

## O que é padrão e o que é recomendação nossa

| Item | Situação | Por quê |
|---|---|---|
| Frontmatter, `type`, `title`, `description`, `resource`, `tags` | OKF | — |
| `generated`, `verified`, níveis de confiança, `status`, `stale_after`, `sources` | OKF v0.2 | — |
| `index.md`, `log.md`, links, IDs, notas de rodapé | OKF | — |
| Dono por pasta | `CODEOWNERS` (GitHub e GitLab) | Memória sem dono apodrece; a OKF não define propriedade |
| Seção `# Relacionados` com verbos | convenção de texto | Dá sentido aos links sem sair do padrão |
| Trecho literal na nota de rodapé | convenção de texto | Permite conferir a fonte |
| Seções por tipo | recomendação | Conceitos completos; a OKF não exige seções |
| Campos que recomendamos preencher (`title`, `description`, `generated`, `sources`) | recomendação | Sem eles não dá para medir confiança |
| `evals/*.yaml` | fora do escopo da OKF | Medir acurácia ([05](05-evals.md)); não afeta a conformidade |

Nenhum conceito tem campo fora da OKF. Qualquer leitor do padrão lê o bundle inteiro sem perder nada.

### O que o validador faz

| Saída | Quando | Efeito |
|---|---|---|
| **ERRO** | Viola a OKF v0.2 (frontmatter, `type`, `index.md`, `log.md`, formato de `generated`, `verified`, `status`, `stale_after`, `sources`) ou há segredo no repo | CI falha |
| **AVISO** | Não segue uma recomendação nossa (tipos, seções, campos recomendados, revisão humana por risco, trecho literal, `stale_after` no que o agente escreve) ou tem link quebrado, que a OKF manda tolerar | CI passa; o revisor decide |

Exceção: na rodada semanal agendada (`--strict`), `stale_after` vencido no bundle `knowledge/` vira erro, para o time ser avisado.

## O que NÃO entra no bundle

| Não entra | Onde fica |
|---|---|
| Transcrições de reunião, logs brutos | Fora do repo, com retenção curta ([07](07-governance.md)) |
| Instruções de um repo específico | `AGENTS.md` do repo |
| Procedimentos executáveis por agente (`SKILL.md`) | Plugin ou skills do time; o `Runbook` aponta para a skill |
| Preferências pessoais | `~/.claude/CLAUDE.md` ou `CLAUDE.local.md` |
| Segredos, dados pessoais | Nunca |
