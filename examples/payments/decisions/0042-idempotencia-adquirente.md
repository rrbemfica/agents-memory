---
type: Decision
title: "ADR-0042: Idempotency-key obrigatória em chamadas a adquirentes"
description: Toda chamada a adquirente leva uma idempotency-key; retries ficam na fila.
tags: [idempotencia, adquirente, money]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-05-20T15:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-05-20T15:00:00Z }
sources:
  - id: pr-412
    resource: https://github.com/example-org/payments-api/pull/412
    title: PR 412, remoção do retry no adapter
    quote: "retry no adapter gerou cobrança duplicada em produção"
owner: team:pagamentos
relations:
  decidesAbout: [/rules/idempotency-key-obrigatoria, /services/payments-api]
---
# Contexto
Retries no adapter do adquirente, sem chave de idempotência, geraram cobranças duplicadas.[^pr-412]

# Decisão
Toda chamada a adquirente envia `idempotencyKey` derivada do ID da cobrança. Retries acontecem só na fila.

# Alternativas rejeitadas
- Deduplicar depois, no ledger: o cliente já teria sido cobrado duas vezes.

# Consequências
Adapters ficam sem lógica de retry; a fila precisa de backoff configurado.

# Revisitar quando
Algum adquirente não suportar idempotência nativa.

[^pr-412]: PR 412, remoção do retry no adapter
