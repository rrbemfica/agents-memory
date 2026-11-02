---
type: BusinessRule
title: Idempotency-key obrigatória em chamadas a adquirentes
description: Nenhuma chamada a adquirente sai sem idempotency-key.
tags: [idempotencia]
timestamp: 2026-05-20
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: code
    ref: payments-api:src/acquirers/base.ts#AcquirerClient.send
  - kind: adr
    ref: examples/payments/decisions/0042-idempotencia-adquirente.md
relations:
  partOf: [examples/payments/index.md]
---
## Regra
Toda requisição a um adquirente inclui `idempotencyKey` derivada do ID da cobrança.

## Motivo
Sem ela, um retry cobra o cliente duas vezes ([ADR-0042](../decisions/0042-idempotencia-adquirente.md)).
