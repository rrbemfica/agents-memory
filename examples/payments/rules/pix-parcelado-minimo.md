---
type: Business Rule
title: Pix parcelado exige valor mínimo de R$ 100
description: Cobranças abaixo de R$ 100 não podem usar Pix parcelado.
tags: [pix, parcelamento, money]
status: stable
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-30T16:00:00Z }
verified:
  - { by: human:tl-pagamentos, at: 2026-10-31T10:00:00Z }
  - { by: process:memory-evals, at: 2026-11-01T06:00:00Z }
stale_after: 2027-04-30T00:00:00Z
sources:
  - id: codigo
    resource: payments-api:src/rules/installments.ts#validateMinimumAmount
  - id: adr-0057
    resource: /decisions/0057-pix-parcelado
    title: ADR-0057
---
# Regra
Uma cobrança só pode ser parcelada via Pix parcelado se o valor total for maior ou igual a R$ 100,00.[^codigo]

# Motivo
Abaixo disso o custo por parcela inviabiliza a operação ([ADR-0057](../decisions/0057-pix-parcelado.md)).[^adr-0057]

# Relacionados
- Usa o termo [Pix parcelado](../terms/pix-parcelado.md)

[^codigo]: payments-api, validateMinimumAmount
[^adr-0057]: ADR-0057
