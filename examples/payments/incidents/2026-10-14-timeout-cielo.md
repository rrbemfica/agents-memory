---
type: Incident
title: "2026-10-14: Timeout na Cielo derrubou cobranças de cartão"
description: Timeout de 30 s segurou conexões e esgotou o pool durante o pico.
tags: [timeout, adquirente]
timestamp: 2026-10-15
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: doc
    ref: https://example.org/postmortems/2026-10-14
relations:
  partOf: [examples/payments/index.md]
  causedBy: [examples/payments/services/cielo.md]
  produced: [examples/payments/runbooks/rollback-pix.md]
---
## Resumo
Latência alta na Cielo, somada a um timeout de 30 s, esgotou o pool de conexões da payments-api.

## Impacto
~40 minutos com falha em cobranças de cartão no horário de pico.

## Causa
Timeout longo demais para o volume de pico; conexões presas.

## Lições
- Timeout reduzido para 15 s (ver [Cielo](../services/cielo.md)).
- Procedimento de reversão documentado em [rollback de cobranças Pix](../runbooks/rollback-pix.md).
