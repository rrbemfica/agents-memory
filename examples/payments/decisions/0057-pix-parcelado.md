---
type: Decision
title: "ADR-0057: Pix parcelado com mínimo de R$ 100"
description: Parcelamento via Pix parcelado, apenas para cobranças a partir de R$ 100.
tags: [pix, parcelamento]
timestamp: 2026-10-30
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: meeting
    ref: examples/payments/meetings/2026-w44-produto.md
    quote: "abaixo de 100 reais o custo da operação não fecha"
relations:
  partOf: [examples/payments/index.md]
  supersedes: [examples/payments/decisions/0031-parcelamento-proprio.md]
  decidesAbout: [examples/payments/rules/pix-parcelado-minimo.md]
  usesTerm: [examples/payments/terms/pix-parcelado.md]
---
## Contexto
O parcelamento próprio ([ADR-0031](0031-parcelamento-proprio.md)) gerou risco de crédito. O Pix parcelado transfere o financiamento a uma instituição parceira.

## Decisão
Oferecer [Pix parcelado](../terms/pix-parcelado.md) só para cobranças a partir de R$ 100.

## Alternativas rejeitadas
- Manter parcelamento próprio: risco de crédito.
- Pix parcelado sem valor mínimo: custo por parcela inviável abaixo de R$ 100.

## Consequências
Cobranças abaixo de R$ 100 não podem ser parceladas.

## Revisitar quando
O custo por parcela da instituição parceira cair abaixo de R$ 0,50.
