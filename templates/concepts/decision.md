---
type: Decision
title: "ADR-NNNN: <decisão em uma frase>"
description: <uma frase: o que foi decidido>
tags: []                     # security | compliance | money | external-source exigem verified por human:
status: draft                # draft | stable | deprecated
generated: { by: <human:id | process:id | agente/versão>, at: AAAA-MM-DDThh:mm:ssZ }
# verified:                  # quem confirmou; human: = revisado por humano
#   - { by: human:<id>, at: AAAA-MM-DDThh:mm:ssZ }
# stale_after: AAAA-MM-DDThh:mm:ssZ   # obrigatório se gerado por agente sem verified
sources:
  - id: <chave>
    resource: <URL ou ID de conceito, ex.: /domains/<d>/meetings/...>
    title: <rótulo da fonte>
    quote: "<trecho literal da fonte>"   # obrigatório em Decision
owner: team:<time>
relations:
  decidesAbout: []
  supersedes: []
---
# Contexto
<O problema e as forças em jogo.>[^<chave>]

# Decisão
<O que foi decidido.>

# Alternativas rejeitadas
- <alternativa>: <por que foi rejeitada>

# Consequências
<Custos e efeitos aceitos.>

# Revisitar quando
<Condição que justificaria rever esta decisão.>

[^<chave>]: <rótulo da fonte>
