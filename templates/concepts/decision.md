---
type: Decision
title: "ADR-NNNN: <decisão em uma frase>"
description: <uma frase: o que foi decidido>
tags: []                     # security | compliance | money | external-source pedem verified por human: (recomendado)
status: draft                # draft | stable | deprecated
generated: { by: <human:id | process:id | agente/versão>, at: AAAA-MM-DDThh:mm:ssZ }
# verified:                  # quem confirmou; human: = revisado por humano
#   - { by: human:<id>, at: AAAA-MM-DDThh:mm:ssZ }
# stale_after: AAAA-MM-DDThh:mm:ssZ   # recomendado se escrito por agente sem verified
sources:
  - id: <chave>
    resource: <URL ou ID de conceito, ex.: /domains/<d>/meetings/...>
    title: <rótulo da fonte>
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

# Relacionados
- Substitui [ADR-NNNN](NNNN-<slug>.md)
- Decide sobre [<conceito>](../<pasta>/<slug>.md)

[^<chave>]: <rótulo da fonte>: "<trecho literal da fonte>"
<!-- Em Decision, recomendamos ao menos uma nota de rodapé com o trecho literal entre aspas. -->
