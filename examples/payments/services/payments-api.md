---
type: Service
title: payments-api
description: Recebe cobranças de cartão e Pix, chama o adquirente e registra no ledger.
tags: [api]
timestamp: 2026-10-30
resource: https://github.com/example-org/payments-api
owner: time-pagamentos
status: active
trust: canonical
last_verified: 2026-11-01
sources:
  - kind: code
    ref: payments-api:src/routes/charge.ts#createCharge
relations:
  partOf: [examples/payments/index.md]
  dependsOn: [examples/payments/services/ledger.md, examples/payments/services/cielo.md]
  implements:
    - examples/payments/rules/pix-parcelado-minimo.md
    - examples/payments/rules/idempotency-key-obrigatoria.md
---
## Responsabilidade
Ponto de entrada de toda cobrança. Valida, chama o adquirente e registra o resultado no [ledger](ledger.md). Não calcula tarifas (isso é do billing).

## Interfaces
- Entrada: `POST /charges`
- Saída: chamada ao adquirente; evento `charge.completed` na fila

## Armadilhas
- Retry é feito pela fila, não no adapter do adquirente ([ADR-0042](../decisions/0042-idempotencia-adquirente.md)).
