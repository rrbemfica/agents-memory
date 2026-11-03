---
type: Runbook
title: <Como fazer X>
description: <uma frase>
tags: []
status: draft                # draft | stable | deprecated
generated: { by: <human:id | process:id | agente/versão>, at: AAAA-MM-DDThh:mm:ssZ }
# verified:                  # quem confirmou; human: = revisado por humano
#   - { by: human:<id>, at: AAAA-MM-DDThh:mm:ssZ }
# stale_after: AAAA-MM-DDThh:mm:ssZ   # recomendado se escrito por agente sem verified
sources:
  - id: origem
    resource: <ID do incidente, doc ou skill>
    title: <rótulo>
---
# Quando usar
<Sintoma ou situação.>[^origem]

# Passos
1. <passo verificável>

# Como verificar
<Como saber que deu certo.>

[^origem]: <rótulo>
