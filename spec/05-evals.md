# 05 · Evals: medindo acurácia

Não avaliamos se uma nota *parece* boa (rubrica). Avaliamos se ela **produz a resposta certa**, contra uma resposta-ouro que vem **da fonte, não da nota**.

> **Camada nossa, recomendada, não obrigatória.** Nem o AGENTS.md nem a OKF definem evals. A OKF só oferece onde registrar o resultado: um item em `verified` com ator `process:` (nível "confirmado por máquina"). Enquanto o runner não existir, evals são **recomendados**: o validador confere o formato quando existem, mas nenhum domínio é obrigado a tê-los. Tornar obrigatório entra por ADR, depois que o runner estiver rodando.

## Três níveis

| Nível | Pergunta | Resposta-ouro vem de | Onde fica | Status |
|---|---|---|---|---|
| **Domínio** | O agente responde certo às perguntas reais do time? | Humanos, a partir de dúvidas reais (Slack, onboarding, reviews) | `knowledge/domains/<d>/evals/*.yaml` | ✅ formato definido e validado; nada roda ainda |
| **Unitário** | Este conceito está certo e agrega valor? | Gerada da fonte citada, sem ver o conceito | `knowledge/domains/<d>/evals/unit/*.yaml` | 📐 planejado |
| **Tarefa** (replay) | O agente resolve tarefas antigas melhor com a memória? | O diff que foi merged de verdade | fora deste repo | 📐 planejado |

## Formato (domínio e unitário)

```yaml
# knowledge/domains/payments/evals/basic.yaml
- id: pay-001
  question: "Qual o valor mínimo para Pix parcelado?"
  answer: "R$ 100"
  grader: contains            # exact | contains | llm
  source: payments-api:src/rules/installments.ts#validateMinimumAmount
  concepts:                   # IDs dos conceitos que deveriam bastar para responder
    - /domains/payments/rules/pix-parcelado-minimo
```

| Campo | Necessário para o runner | Regra |
|---|---|---|
| `id` | ✅ | Único no repo |
| `question` | ✅ | Pergunta como alguém do time faria |
| `answer` | ✅ | Resposta-ouro, curta |
| `grader` | ✅ | `exact` / `contains` sempre que possível; `llm` só para respostas abertas |
| `source` | ✅ | De onde a resposta-ouro foi tirada (mesmo formato de `sources[].resource`) |
| `concepts` | recomendado | IDs relativos ao bundle; o validador avisa se não existem |

## Como rodar (runner — 📐 a implementar)

Cada pergunta roda em três modos:

| Modo | Mede |
|---|---|
| **Sem memória** (só código) | Linha de base |
| **Com memória** | Acurácia com o bundle |
| **Com memória + código** | Cenário real |

Interpretação por conceito (evals unitários):

| Com o conceito | Sem o conceito | Veredito |
|---|---|---|
| ✅ | ❌ | Correto e útil → mantém e registra `verified: { by: process:memory-evals, at: … }` |
| ✅ | ✅ | Redundante (derivável do código) → remover |
| ❌ | — | Errado ou desatualizado → corrigir ou remover |

## Cuidados

- **Circularidade:** quem gera a resposta-ouro **não vê o conceito**, só a fonte.
- **Perguntas fáceis demais** aparecem no modo "sem memória": se acerta sem, a pergunta não mede nada.
- **Erros plantados:** periodicamente, injetar um conceito propositalmente errado num ambiente de teste e verificar se os evals o pegam.
- **Grader LLM** só compara resposta com resposta-ouro — nunca julga "qualidade".

## Métricas

| Métrica | Meta inicial | Diz |
|---|---|---|
| Acurácia do domínio (com memória) | ≥ 90% | Se a memória responde certo |
| Ganho vs. sem memória | > 0, crescente | Se a memória agrega |
| Acurácia de conceitos revisados por humano (amostra mensal) | ≥ 98% | Se a revisão é rigorosa |
| Acurácia de conceitos confirmados por máquina | ≥ 90% | Se os evals bastam como verificação |
| Acurácia de conceitos não verificados | ≥ 85% | Se as checagens de entrada bastam |
| Meia-vida | medir | Calibra os prazos de `stale_after` em [04](04-lifecycle.md#prazos-padrão-de-stale_after) |
| Recall de erros plantados | ≥ 90% | Se o sistema detecta erro |

## Quem escreve evals de domínio

O time dono do domínio, a partir de **dúvidas reais**. Recomendado: começar com umas 20 perguntas quando o domínio tiver conteúdo suficiente e acrescentar toda dúvida que um agente ou pessoa errou. É o principal trabalho humano recorrente do sistema — e também documenta o que o time precisa saber.
