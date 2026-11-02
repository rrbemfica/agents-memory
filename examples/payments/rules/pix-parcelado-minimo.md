---
type: BusinessRule
title: Pix parcelado exige valor mínimo de R$ 100
description: Cobranças abaixo de R$ 100 não podem usar Pix parcelado.
tags: [pix, parcelamento]
timestamp: 2026-10-30
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: code
    ref: payments-api:src/rules/installments.ts#validateMinimumAmount
  - kind: adr
    ref: examples/payments/decisions/0057-pix-parcelado.md
relations:
  partOf: [examples/payments/index.md]
  usesTerm: [examples/payments/terms/pix-parcelado.md]
---
## Regra
Uma cobrança só pode ser parcelada via Pix parcelado se o valor total for maior ou igual a R$ 100,00.

## Motivo
Abaixo disso o custo por parcela inviabiliza a operação ([ADR-0057](../decisions/0057-pix-parcelado.md)).
