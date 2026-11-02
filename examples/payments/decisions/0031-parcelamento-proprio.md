---
type: Decision
title: "ADR-0031: Parcelamento financiado pela própria empresa"
description: Oferecer parcelamento sem juros financiado pela própria empresa.
tags: [parcelamento, money]
status: deprecated
generated: { by: human:pm-pagamentos, at: 2026-03-10T15:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-03-11T10:00:00Z }
sources:
  - id: ata-marco
    resource: https://example.org/atas/2026-03-10-produto
    title: Ata da reunião de produto de março
    quote: "vamos testar parcelamento próprio por um trimestre"
owner: team:pagamentos
---
# Contexto
Clientes pediam parcelamento e o adquirente cobrava caro pela antecipação.

# Decisão
Financiar o parcelamento com caixa próprio, como experimento de um trimestre.[^ata-marco]

# Alternativas rejeitadas
- Parcelamento via adquirente: custo de antecipação alto na época.

# Consequências
Risco de crédito assumido pela empresa.

[^ata-marco]: Ata da reunião de produto de março
