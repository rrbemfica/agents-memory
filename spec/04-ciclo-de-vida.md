# 04 · Ciclo de vida de um conceito

```
 CAPTURAR ──► PROPOR ──► CHECAR ──► MERGE ──► USAR ──► MANTER
   fontes      PR com     validador   entra no   agente     fonte mudou?
   brutas      conceito   + evals     nível de   confirma   passou do
                                      confiança  no uso     stale_after?
     ▲                                                          │
     └──────────────────────────────────────────────────────────┘
```

## Níveis de confiança (OKF v0.2)

Não declaramos confiança: ela é **derivada** de `generated` e `verified` (OKF §5.2–5.3).

| Nível | Como chega lá | Exemplo de `verified` |
|---|---|---|
| **não verificado** | Agente escreveu e ninguém confirmou | (ausente) |
| **confirmado por máquina** | Evals do conceito passaram, ou outro agente confirmou contra a fonte no uso | `{ by: process:memory-evals, at: … }` |
| **revisado por humano** | Uma pessoa confirmou (no review do PR ou depois) | `{ by: human:joana, at: … }` |

- Atores (OKF §7): `human:<id>` para pessoas, `process:<id>` para jobs (`process:memory-evals`, `process:memory-gardener`) e `<agente>/<versão>` para agentes (`claude-code/claude-opus-5-5`).
- **Conceito escrito por pessoa** (`generated.by: human:…`) é confiável para quem o escreveu, mas só chega a "revisado por humano" quando aparece em `verified`. O normal é o revisor do PR se registrar ali.
- **Conceito escrito por agente sem `verified`: recomendamos `stale_after`** (padrão: +30 dias). Se ninguém confirmar até lá, ele fica velho e sai.

## Quando pedir revisão humana

Revisão humana em tudo cria fila, e fila vira carimbo. Revisão em nada abre espaço para memória envenenada. A recomendação é pedir humano **onde o erro é caro ou a verificação automática não alcança**. Nenhuma linha abaixo bloqueia o CI: o validador avisa, e quem decide é o revisor do PR.

| Situação | Revisão humana? | Por quê | Como é conferido |
|---|---|---|---|
| `Decision` `stable` | ✅ recomendada | Intenção e escolha não se verificam no código | Validador avisa sem `human:` em `generated.by` ou `verified`. Em `draft`, agentes podem propor. |
| Tags `security`, `compliance`, `money` | ✅ recomendada | Erro caro | Validador avisa sem `verified` por `human:` (exceto em `draft`) |
| Conteúdo de fonte externa (cliente, ticket público, web) | ✅ recomendada | Principal vetor de envenenamento | Tag `external-source`; validador avisa sem `verified` por `human:` (exceto em `draft`) |
| Descontinuar ou substituir conceito revisado por humano | ✅ recomendada | Perde histórico confiável | Revisão do PR pelo `CODEOWNERS` do domínio |
| Conflito entre dois conceitos revisados por humano | ✅ recomendada | Nenhum sistema resolve bem conflitos | Revisão do PR |
| `Term`, `Business Rule`, `Service`, `Runbook`, `Incident`, `Meeting` escritos por agente, com fonte | ❌ | Os evals verificam contra a fonte | Entram como não verificados, com `stale_after`, e sobem de nível pelos evals e pelo uso |
| Atualizar `Service` a partir do código | ❌ | Derivado do código | Regenerado; evals confirmam |

`draft` é a forma de um agente propor algo que pede humano: o conceito existe, aparece como proposta e não vale como regra até alguém revisar.

Resultado esperado: a revisão humana fica concentrada em decisões e no que é arriscado, que deve ser uma fração pequena do volume.

## 1. Capturar

| Gatilho | Conceito típico |
|---|---|
| Fim de sessão de agente | "O que aprendi que não está escrito?" → no máximo **2** conceitos por sessão |
| Plano de feature concluído | `Decision` em `draft`, com alternativas rejeitadas (vai para revisão humana) |
| Comentário de review aceito | `Business Rule` ou linha de `AGENTS.md` |
| Reunião (com consentimento) | `Term`, `Decision` em `draft` e um `Meeting` curto |
| Postmortem fechado | `Incident` + lições como conceitos |
| Merge que muda contrato ou dependência | Atualização de `Service` |

## 2. Propor

- Todo conceito entra **por PR** neste repo.
- Antes de criar, procure conceito existente. Se ele já existe, proponha um **delta** (ou só um novo item em `verified`), não um conceito novo.
- **Nunca reescreva um conceito inteiro** com LLM: mudanças são pontuais e revisáveis no diff.
- Conflito com conceito revisado por humano: o PR **não** sobrescreve; ele vai para revisão humana.
- Registre a mudança no `log.md` do domínio.

## 3. Checar (automático, no CI)

| Checagem | Garante | Status |
|---|---|---|
| `validate.py` | Conformidade OKF v0.2, campos, tipos, links, notas de rodapé, seções, regras de humano, segredos | ✅ implementado |
| Grounding | Cada trecho entre aspas das notas de rodapé existe literalmente na fonte | 📐 planejado |
| Evals do conceito | Responde certo e agrega valor (com e sem memória) → acrescenta `verified: process:memory-evals` | 📐 ver [05](05-evals.md) |
| Evals do domínio | Nada piorou | 📐 ver [05](05-evals.md) |

## 4. Usar

Ordem de leitura do agente, do mais barato ao mais caro:

1. `AGENTS.md` do repo (automático).
2. `index.md` do domínio indicado.
3. Conceitos linkados, sob demanda.
4. Busca ou grafo (MCP), se ainda faltar.

Regras de uso:
- **não verificado** → conferir a fonte antes de agir;
- **passou do `stale_after`** → tratar como desatualizado e avisar;
- **`deprecated`** → não usar; seguir o link "Substituída por".

Se o agente confirmar o conceito contra a fonte, ele pode propor um item em `verified` com o próprio ator. Se for contradito, propõe a correção.

## 5. Manter (gardener)

Job agendado (📐 especificado; `stale_after` vencido já é checado pelo validador):

- **A fonte mudou?** Rodar de novo os evals do conceito. Passou: renova `verified` e `stale_after`. Falhou: abre PR de correção.
- **Passou do `stale_after`?** Renovar se confirmado; senão, remover.
- **Órfão?** Conceito que nenhum `index.md` lista e nenhum outro conceito linka → avisar o dono.
- **Dono não existe mais?** Avisar os donos de `org/`.
- Montar o grafo em memória para achar órfãos e links quebrados.

## Prazos padrão de `stale_after`

| Tipo | Gerado por agente, sem `verified` | Depois de verificado |
|---|---|---|
| `Service` | +30 dias | +90 dias, ou quando a fonte mudar |
| `Business Rule`, `Term` | +60 dias | +180 dias |
| `Decision` | — (recomendamos humano) | sem `stale_after`; só é substituída |
| `Runbook` | +60 dias | +180 dias, ou quando falhar em uso |
| `Incident` | — | sem `stale_after` |
| `Meeting` | +90 dias | +90 dias |

Estes valores são **hipóteses iniciais**. Devem ser recalibrados pela meia-vida medida nos evals ([05](05-evals.md)).
