---
type: Business Rule
title: <regra em uma frase>
description: <uma frase>
tags: []
status: draft                # draft | stable | deprecated
generated: { by: <human:id | process:id | agente/versão>, at: AAAA-MM-DDThh:mm:ssZ }
# verified:                  # quem confirmou; human: = revisado por humano
#   - { by: human:<id>, at: AAAA-MM-DDThh:mm:ssZ }
# stale_after: AAAA-MM-DDThh:mm:ssZ   # obrigatório se gerado por agente sem verified
sources:
  - id: codigo
    resource: <repo>:<caminho>#<símbolo>
owner: team:<time>
relations:
  usesTerm: []
---
# Regra
<Uma frase verificável.>[^codigo]

# Motivo
<Por que a regra existe.>

[^codigo]: <repo>, <símbolo>
