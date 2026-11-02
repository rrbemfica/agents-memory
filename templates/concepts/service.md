---
type: Service
title: <nome-do-servico>
description: <uma frase: o que faz>
resource: <URL do repo ou do sistema>
tags: []                     # use [external] para sistemas de terceiros
status: draft                # draft | stable | deprecated
generated: { by: <human:id | process:id | agente/versão>, at: AAAA-MM-DDThh:mm:ssZ }
# verified:                  # quem confirmou; human: = revisado por humano
#   - { by: human:<id>, at: AAAA-MM-DDThh:mm:ssZ }
# stale_after: AAAA-MM-DDThh:mm:ssZ   # obrigatório se gerado por agente sem verified
sources:
  - id: codigo
    resource: <repo>:<caminho>
owner: team:<time>
relations:
  dependsOn: []
  implements: []
---
# Responsabilidade
<O que este serviço faz e o que NÃO faz.>[^codigo]

# Interfaces
- Entrada: <API, fila ou evento>
- Saída: <API, fila ou evento>

# Armadilhas
- <o que já deu problema>

[^codigo]: <repo>
