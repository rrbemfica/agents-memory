---
type: Term
title: Estorno
description: Devolução de valor iniciada pela própria empresa.
tags: [refund, devolucao]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-09-01T12:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-09-01T12:00:00Z }
sources:
  - id: refund
    resource: payments-api:src/routes/refund.ts#createRefund
---
# Definição
Nós decidimos devolver o valor ao cliente, total ou parcialmente.[^refund]

# Exemplo
"Fizemos estorno parcial porque um item não foi entregue."

# Não confundir com
- [Chargeback](chargeback.md): reversão forçada pelo banco emissor.

[^refund]: payments-api, createRefund
