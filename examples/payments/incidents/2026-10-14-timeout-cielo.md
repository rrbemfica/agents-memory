---
type: Incident
title: "2026-10-14: Timeout na Cielo derrubou cobranças de cartão"
description: Timeout de 30 s segurou conexões e esgotou o pool durante o pico.
tags: [timeout, adquirente]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-10-15T12:00:00Z }
verified: { by: human:sre, at: 2026-10-15T18:00:00Z }
sources:
  - id: postmortem
    resource: https://example.org/postmortems/2026-10-14
    title: Postmortem original
---
# Resumo
Latência alta na Cielo, somada a um timeout de 30 s, esgotou o pool de conexões da payments-api.[^postmortem]

# Impacto
Cerca de 40 minutos com falha em cobranças de cartão no horário de pico.

# Causa
Timeout longo demais para o volume de pico; conexões presas.

# Lições
- Timeout reduzido para 15 s (ver [Cielo](../services/cielo.md)).
- Procedimento de reconciliação documentado em [reconciliar cobranças de cartão](../runbooks/reconciliar-cartao-falha-adquirente.md).

# Relacionados
- Causado por [Cielo (adquirente)](../services/cielo.md)
- Gerou [Reconciliar cobranças de cartão após falha do adquirente](../runbooks/reconciliar-cartao-falha-adquirente.md)

[^postmortem]: Postmortem original
