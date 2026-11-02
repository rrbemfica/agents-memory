---
type: Service
title: payments-api
description: Recebe cobranças de cartão e Pix, chama o adquirente e registra no ledger.
resource: https://github.com/example-org/payments-api
tags: [api]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-10-30T12:00:00Z }
verified:
  - { by: human:tl-pagamentos, at: 2026-10-30T12:00:00Z }
  - { by: process:memory-evals, at: 2026-11-01T06:00:00Z }
stale_after: 2027-01-30T00:00:00Z
sources:
  - id: charge-route
    resource: payments-api:src/routes/charge.ts#createCharge
owner: team:pagamentos
relations:
  dependsOn: [/services/ledger, /services/cielo]
  implements: [/rules/pix-parcelado-minimo, /rules/idempotency-key-obrigatoria]
---
# Responsabilidade
Ponto de entrada de toda cobrança. Valida, chama o adquirente e registra o resultado no [ledger](ledger.md). Não calcula tarifas (isso é do billing).[^charge-route]

# Interfaces
- Entrada: `POST /charges`
- Saída: chamada ao adquirente; evento `charge.completed` na fila

# Armadilhas
- Retry é feito pela fila, não no adapter do adquirente ([ADR-0042](../decisions/0042-idempotencia-adquirente.md)).

[^charge-route]: payments-api, rota de cobrança
