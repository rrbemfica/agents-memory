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
---
# Contexto
Clientes pediam parcelamento e o adquirente cobrava caro pela antecipação.

# Decisão
Financiar o parcelamento com caixa próprio, como experimento de um trimestre.[^ata-marco]

# Alternativas rejeitadas
- Parcelamento via adquirente: custo de antecipação alto na época.

# Consequências
Risco de crédito assumido pela empresa.

# Relacionados
- Substituída por [ADR-0057: Pix parcelado com mínimo de R$ 100](0057-pix-parcelado.md)

[^ata-marco]: Ata da reunião de produto de março: "vamos testar parcelamento próprio por um trimestre"
