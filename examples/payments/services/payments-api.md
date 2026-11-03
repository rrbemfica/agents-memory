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
---
# Responsabilidade
Ponto de entrada de toda cobrança. Valida, chama o adquirente e registra o resultado no [ledger](ledger.md). Não calcula tarifas (isso é do billing).[^charge-route]

# Interfaces
- Entrada: `POST /charges`
- Saída: chamada ao adquirente; evento `charge.completed` na fila

# Armadilhas
- Retry é feito pela fila, não no adapter do adquirente ([ADR-0042](../decisions/0042-idempotencia-adquirente.md)).

# Relacionados
- Depende de [ledger](ledger.md)
- Depende de [Cielo (adquirente)](cielo.md)
- Implementa [Pix parcelado exige valor mínimo de R$ 100](../rules/pix-parcelado-minimo.md)
- Implementa [Idempotency-key obrigatória em chamadas a adquirentes](../rules/idempotency-key-obrigatoria.md)

[^charge-route]: payments-api, rota de cobrança
