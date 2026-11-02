---
type: BusinessRule
title: <regra em uma frase>
description: <uma frase>
tags: []
timestamp: YYYY-MM-DD
owner: <time>
status: active
trust: canonical             # inferred se escrito por agente sem confirmação
# expires: YYYY-MM-DD        # obrigatório se trust: inferred
sources:
  - kind: code
    ref: <repo>:<caminho>#<símbolo>
relations:
  partOf: [domains/<dominio>/index.md]
  usesTerm: []
---
## Regra
<Uma frase verificável.>

## Motivo
<Por que a regra existe.>
