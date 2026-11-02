---
type: Business Rule
title: Idempotency-key obrigatória em chamadas a adquirentes
description: Nenhuma chamada a adquirente sai sem idempotency-key.
tags: [idempotencia, money]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-05-20T15:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-05-20T15:00:00Z }
stale_after: 2026-11-20T00:00:00Z
sources:
  - id: codigo
    resource: payments-api:src/acquirers/base.ts#AcquirerClient.send
  - id: adr-0042
    resource: /decisions/0042-idempotencia-adquirente
    title: ADR-0042
owner: team:pagamentos
---
# Regra
Toda requisição a um adquirente inclui `idempotencyKey` derivada do ID da cobrança.[^codigo]

# Motivo
Sem ela, um retry cobra o cliente duas vezes ([ADR-0042](../decisions/0042-idempotencia-adquirente.md)).[^adr-0042]

[^codigo]: payments-api, AcquirerClient.send
[^adr-0042]: ADR-0042
