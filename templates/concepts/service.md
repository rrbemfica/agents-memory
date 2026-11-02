---
type: Service
title: <nome-do-servico>
description: <uma frase: o que faz>
tags: []                     # use [external] para sistemas de terceiros
timestamp: YYYY-MM-DD
resource: <URL do repo ou do sistema>
owner: <time>
status: active
trust: canonical
sources:
  - kind: code
    ref: <repo>:<caminho>
relations:
  partOf: [domains/<dominio>/index.md]
  dependsOn: []
  implements: []
---
## Responsabilidade
<O que este serviço faz e o que NÃO faz.>

## Interfaces
- Entrada: <API/fila/evento>
- Saída: <API/fila/evento>

## Armadilhas
- <o que já deu problema>
