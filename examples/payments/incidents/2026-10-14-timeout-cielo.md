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
- Procedimento de reversão documentado em [rollback de cobranças Pix](../runbooks/rollback-pix.md).

# Relacionados
- Causado por [Cielo (adquirente)](../services/cielo.md)
- Gerou [Rollback de cobranças Pix](../runbooks/rollback-pix.md)

[^postmortem]: Postmortem original
