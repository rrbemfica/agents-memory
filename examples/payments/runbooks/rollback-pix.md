---
type: Runbook
title: Rollback de cobranças Pix
description: Como reverter um lote de cobranças Pix processadas com erro.
tags: [pix, rollback]
timestamp: 2026-10-16
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: incident
    ref: examples/payments/incidents/2026-10-14-timeout-cielo.md
relations:
  partOf: [examples/payments/index.md]
  usesTerm: [examples/payments/terms/estorno.md]
---
## Quando usar
Um lote de cobranças Pix foi confirmado ao cliente mas não registrado no ledger (ou o contrário).

## Passos
1. Pausar o consumidor da fila `charge.completed`.
2. Listar as cobranças afetadas pelo intervalo do incidente.
3. Para cada uma, gerar [estorno](../terms/estorno.md) pelo endpoint de refund (nunca editar o ledger).
4. Retomar o consumidor.

## Como verificar
A soma dos lançamentos do intervalo no ledger fecha em zero e não há cobrança sem lançamento.
