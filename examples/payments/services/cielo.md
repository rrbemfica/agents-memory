---
type: Service
title: Cielo (adquirente)
description: Adquirente externo usado para cobranças de cartão.
resource: https://developercielo.github.io
tags: [external, adquirente]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-10-15T12:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-10-15T12:00:00Z }
stale_after: 2027-01-15T00:00:00Z
sources:
  - id: incidente
    resource: /incidents/2026-10-14-timeout-cielo
    title: Postmortem do timeout na Cielo
---
# Responsabilidade
Autoriza e captura transações de cartão. Sistema de terceiros.

# Armadilhas
- Latência sobe em horário de pico; o timeout da integração é 15 s (antes 30 s).[^incidente]

[^incidente]: Postmortem do timeout na Cielo
