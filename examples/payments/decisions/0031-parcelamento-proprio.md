---
type: Decision
title: "ADR-0031: Parcelamento financiado pela própria empresa"
description: Oferecer parcelamento sem juros financiado pela própria empresa.
tags: [parcelamento]
timestamp: 2026-03-10
owner: time-pagamentos
status: superseded
trust: canonical
sources:
  - kind: meeting
    ref: https://example.org/atas/2026-03-10-produto
    quote: "vamos testar parcelamento próprio por um trimestre"
relations:
  partOf: [examples/payments/index.md]
---
## Contexto
Clientes pediam parcelamento e o adquirente cobrava caro pela antecipação.

## Decisão
Financiar o parcelamento com caixa próprio, como experimento de um trimestre.

## Alternativas rejeitadas
- Parcelamento via adquirente: custo de antecipação alto na época.

## Consequências
Risco de crédito assumido pela empresa.
