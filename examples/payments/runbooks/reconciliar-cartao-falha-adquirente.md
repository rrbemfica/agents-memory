---
type: Runbook
title: Reconciliar cobranças de cartão após falha do adquirente
description: Como reconciliar cobranças de cartão que ficaram sem resposta quando o adquirente falhou.
tags: [cartao, adquirente, money]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-10-16T12:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-10-16T12:00:00Z }
stale_after: 2027-04-16T00:00:00Z
sources:
  - id: incidente
    resource: /incidents/2026-10-14-timeout-cielo
    title: Postmortem do timeout na Cielo
---
# Quando usar
Timeout ou indisponibilidade do adquirente deixou cobranças de cartão sem resposta: o cliente pode ter sido cobrado sem registro no ledger, ou o contrário.[^incidente]

# Passos
1. Pausar o consumidor da fila `charge.completed`.
2. Listar as cobranças sem resposta no intervalo do incidente.
3. Consultar cada uma no adquirente pela [idempotency-key](../rules/idempotency-key-obrigatoria.md).
4. Capturada no adquirente e ausente no ledger: publicar o `charge.completed` que faltou. Ausente no adquirente: marcar como falha e avisar o cliente. Capturada duas vezes: gerar [estorno](../terms/estorno.md) pelo endpoint de refund (nunca editar o ledger).
5. Retomar o consumidor.

# Como verificar
Toda cobrança do intervalo tem o mesmo estado no adquirente e no ledger, e nenhuma ficou sem lançamento.

# Relacionados
- Aplica-se a [Cielo (adquirente)](../services/cielo.md)
- Usa o termo [Estorno](../terms/estorno.md)

[^incidente]: Postmortem do timeout na Cielo
