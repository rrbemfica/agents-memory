---
type: Meeting
title: Produto Pagamentos, semana 44/2026
description: Definição do Pix parcelado e do valor mínimo.
tags: [produto]
timestamp: 2026-10-30
expires: 2027-01-28
participants: [time-pagamentos, produto]
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: doc
    ref: https://example.org/atas/2026-10-30-produto
relations:
  partOf: [examples/payments/index.md]
  produced:
    - examples/payments/decisions/0057-pix-parcelado.md
    - examples/payments/terms/pix-parcelado.md
---
- Decidido: Pix parcelado com mínimo de R$ 100 (→ [ADR-0057](../decisions/0057-pix-parcelado.md))
- Termo novo: Pix parcelado (→ [glossário](../terms/pix-parcelado.md))
- Pendente: limite máximo de parcelas
