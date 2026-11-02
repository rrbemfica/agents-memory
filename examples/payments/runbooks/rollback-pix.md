---
type: Runbook
title: Rollback de cobranças Pix
description: Como reverter um lote de cobranças Pix processadas com erro.
tags: [pix, rollback, money]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-10-16T12:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-10-16T12:00:00Z }
stale_after: 2027-04-16T00:00:00Z
sources:
  - id: incidente
    resource: /incidents/2026-10-14-timeout-cielo
    title: Postmortem do timeout na Cielo
owner: team:pagamentos
relations:
  usesTerm: [/terms/estorno]
---
# Quando usar
Um lote de cobranças Pix foi confirmado ao cliente mas não registrado no ledger (ou o contrário).[^incidente]

# Passos
1. Pausar o consumidor da fila `charge.completed`.
2. Listar as cobranças afetadas pelo intervalo do incidente.
3. Para cada uma, gerar [estorno](../terms/estorno.md) pelo endpoint de refund (nunca editar o ledger).
4. Retomar o consumidor.

# Como verificar
A soma dos lançamentos do intervalo no ledger fecha em zero e não há cobrança sem lançamento.

[^incidente]: Postmortem do timeout na Cielo
