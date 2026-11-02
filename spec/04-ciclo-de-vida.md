# 04 · Ciclo de vida de um conceito

```
 CAPTURAR ──► PROPOR ──► VERIFICAR ──► MERGE ──► USAR ──► MANTER
   fontes      PR com     lint +        inferred   agente     gardener:
   brutas      candidato  evals         ou         confirma   fonte mudou?
                                        canonical  no uso     expirou?
     ▲                                                          │
     └──────────────────────────────────────────────────────────┘
```

## Níveis de confiança

| `trust` | Significa | Como o agente trata |
|---|---|---|
| `canonical` | Confirmado por humano **ou** por verificação automática forte (ver abaixo) | Pode seguir como regra |
| `inferred` | Escrito por agente, com fonte, passou nas checagens, ainda não confirmado | **Pista**: verifica a fonte antes de agir; expira se não for confirmado |

Material bruto (transcrição, log) **não** é conceito e nunca é servido como instrução.

## 1. Capturar

Gatilhos que geram candidatos:

| Gatilho | Candidato típico |
|---|---|
| Fim de sessão de agente | "O que aprendi que não está escrito?" → no máximo **2** candidatos por sessão |
| Plano de feature concluído | `Decision` candidata, com alternativas rejeitadas |
| Comentário de review aceito | `BusinessRule` ou linha de `AGENTS.md` |
| Reunião (com consentimento) | `Term`, `Decision` candidatos + `Meeting` curto |
| Postmortem fechado | `Incident` + lições como conceitos |
| Merge que muda contrato/dependência | Atualização de `Service` |

## 2. Propor

- Todo candidato entra **por PR** neste repo, com `status: candidate` ou `trust: inferred`.
- Antes de criar, procurar conceito existente: se já existe, propor **delta** nele (ou só renovar `last_verified`), não um novo.
- **Nunca reescrever um conceito inteiro** com LLM. Mudanças são pontuais e revisáveis no diff.
- Conflito com conceito `canonical` → o PR **não** sobrescreve; abre como conflito (ver "o que exige humano").
- Registrar no `log.md` do bundle.

## 3. Verificar (automático, no CI)

| Checagem | O que garante | Status |
|---|---|---|
| `validate.py` | Estrutura, tipo, campos, relações válidas, links, seções, segredos | ✅ implementado |
| Grounding | Cada `quote` existe literalmente na fonte | 📐 planejado (hoje: obrigatoriedade do campo) |
| Evals unitários | O conceito responde certo e agrega valor (com vs. sem) | 📐 ver [05](05-evals.md) |
| Evals do domínio | Nada piorou no domínio | 📐 ver [05](05-evals.md) |

## 4. Merge

| Situação | Quem aprova | Resultado |
|---|---|---|
| Candidato de agente, risco baixo, checagens ok | Ninguém (auto-merge) | `trust: inferred`, `expires` = +30 dias |
| Conceito escrito por humano em PR revisado | Revisor do PR | `trust: canonical` |
| Conceito derivado de algo já aprovado (PR merged, ADR aceito, postmortem fechado) com `quote` | Ninguém | `trust: canonical` — a aprovação já aconteceu na fonte |
| Risco alto (ver abaixo) | Dono do domínio/segurança | conforme revisão |

### O que sempre exige humano

1. Regras de **segurança, compliance ou dinheiro**.
2. Conteúdo vindo de **fonte externa** (cliente, ticket público, web).
3. **Conflito** entre conceitos `canonical`.
4. **Substituir ou remover** conceito `canonical`.
5. `Decision` nova **sem fonte humana**.

## 5. Usar

Ordem de leitura do agente (do mais barato ao mais caro):

1. `AGENTS.md` do repo (automático).
2. `index.md` do domínio indicado.
3. Conceitos específicos linkados (sob demanda).
4. Busca/grafo (MCP) se ainda faltar.

Ao usar um conceito `inferred`, o agente confere a fonte. Confirmou → pode propor renovação (`last_verified`, `expires`). Contradito → propõe correção.

**Promoção a `canonical`:** 3 confirmações independentes no uso sem contradição, ou aprovação humana.

## 6. Manter (gardener)

Job agendado (📐 especificado; a expiração já é checada pelo validador):

- **Fonte mudou?** Se o símbolo/arquivo citado em `sources` mudou, marcar para reverificação (rodar os evals do conceito).
- **Expirou?** `inferred` ou `Meeting` com `expires` no passado → remover (ou renovar se confirmado).
- **Órfão?** Conceito que nenhum `index.md` ou relação alcança → avisar o dono.
- **Sem dono ativo?** `owner` que não existe mais → avisar `org/`.
- **Grafo e backlinks** regenerados (`build_graph.py`).

## Prazos padrão

| Tipo | `inferred` expira em | Reverificação de `canonical` |
|---|---|---|
| `Service` | 30 dias | quando a fonte muda |
| `BusinessRule`, `Term` | 60 dias | 180 dias |
| `Decision` | — (exige fonte humana) | não expira; só é substituída |
| `Runbook` | 60 dias | 180 dias ou quando falhar em uso |
| `Incident` | — | não expira |
| `Meeting` | sempre 90 dias | — |

Estes valores são **hipóteses iniciais**. Devem ser recalibrados pela meia-vida medida nos evals ([05](05-evals.md)).
