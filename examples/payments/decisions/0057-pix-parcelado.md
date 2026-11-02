---
type: Decision
title: "ADR-0057: Pix parcelado com mínimo de R$ 100"
description: Parcelamento via Pix parcelado, apenas para cobranças a partir de R$ 100.
tags: [pix, parcelamento, money]
status: stable
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-30T16:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-10-31T10:00:00Z }
sources:
  - id: reuniao-w44
    resource: /meetings/2026-w44-produto
    title: Reunião de produto W44
    author: team:produto
    quote: "abaixo de 100 reais o custo da operação não fecha"
owner: team:pagamentos
relations:
  supersedes: [/decisions/0031-parcelamento-proprio]
  decidesAbout: [/rules/pix-parcelado-minimo]
  usesTerm: [/terms/pix-parcelado]
---
# Contexto
O parcelamento próprio ([ADR-0031](0031-parcelamento-proprio.md)) gerou risco de crédito. O Pix parcelado transfere o financiamento a uma instituição parceira.

# Decisão
Oferecer [Pix parcelado](../terms/pix-parcelado.md) só para cobranças a partir de R$ 100.[^reuniao-w44]

# Alternativas rejeitadas
- Manter parcelamento próprio: risco de crédito.
- Pix parcelado sem valor mínimo: custo por parcela inviável abaixo de R$ 100.

# Consequências
Cobranças abaixo de R$ 100 não podem ser parceladas.

# Revisitar quando
O custo por parcela da instituição parceira cair abaixo de R$ 0,50.

[^reuniao-w44]: Reunião de produto W44
