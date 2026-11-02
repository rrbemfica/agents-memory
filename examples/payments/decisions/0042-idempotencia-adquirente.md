---
type: Decision
title: "ADR-0042: Idempotency-key obrigatória em chamadas a adquirentes"
description: Toda chamada a adquirente leva uma idempotency-key; retries ficam na fila.
tags: [idempotencia, adquirente]
timestamp: 2026-05-20
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: pr
    ref: https://github.com/example-org/payments-api/pull/412
    quote: "retry no adapter gerou cobrança duplicada em produção"
relations:
  partOf: [examples/payments/index.md]
  decidesAbout:
    - examples/payments/rules/idempotency-key-obrigatoria.md
    - examples/payments/services/payments-api.md
---
## Contexto
Retries no adapter do adquirente, sem chave de idempotência, geraram cobranças duplicadas.

## Decisão
Toda chamada a adquirente envia `idempotencyKey` derivada do ID da cobrança. Retries acontecem só na fila.

## Alternativas rejeitadas
- Deduplicar depois, no ledger: o cliente já teria sido cobrado duas vezes.

## Consequências
Adapters ficam sem lógica de retry; a fila precisa de backoff configurado.

## Revisitar quando
Algum adquirente não suportar idempotência nativa.
