---
type: Incident
title: "AAAA-MM-DD: <resumo do incidente>"
description: <uma frase>
tags: []
status: draft                # draft | stable | deprecated
generated: { by: <human:id | process:id | agente/versão>, at: AAAA-MM-DDThh:mm:ssZ }
# verified:                  # quem confirmou; human: = revisado por humano
#   - { by: human:<id>, at: AAAA-MM-DDThh:mm:ssZ }
# stale_after: AAAA-MM-DDThh:mm:ssZ   # obrigatório se gerado por agente sem verified
sources:
  - id: postmortem
    resource: <link do postmortem original>
    title: Postmortem original
---
# Resumo
<O que aconteceu.>[^postmortem]

# Impacto
<Quem e quanto foi afetado.>

# Causa
<Causa raiz.>

# Lições
- <lição> → <link para o conceito gerado>

# Relacionados
- Causado por [<servico ou decisão>](../services/<servico>.md)

[^postmortem]: Postmortem original
