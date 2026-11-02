---
type: Term
title: Estorno
description: Devolução de valor iniciada pela própria empresa.
tags: [refund, devolucao]
timestamp: 2026-09-01
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: code
    ref: payments-api:src/routes/refund.ts#createRefund
relations:
  partOf: [examples/payments/index.md]
---
## Definição
Nós decidimos devolver o valor ao cliente, total ou parcialmente.

## Exemplo
"Fizemos estorno parcial porque um item não foi entregue."

## Não confundir com
- [Chargeback](chargeback.md): reversão forçada pelo banco emissor.
