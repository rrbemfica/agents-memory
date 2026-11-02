---
type: Service
title: Cielo (adquirente)
description: Adquirente externo usado para cobranças de cartão.
tags: [external, adquirente]
timestamp: 2026-10-15
resource: https://developercielo.github.io
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: incident
    ref: examples/payments/incidents/2026-10-14-timeout-cielo.md
relations:
  partOf: [examples/payments/index.md]
---
## Responsabilidade
Autoriza e captura transações de cartão. Sistema de terceiros.

## Armadilhas
- Latência sobe em horário de pico; o timeout da integração é 15 s (antes 30 s, ver [incidente](../incidents/2026-10-14-timeout-cielo.md)).
