---
type: Service
title: ledger
description: Registro contábil de dupla entrada de todas as movimentações.
tags: [contabil]
timestamp: 2026-09-01
resource: https://github.com/example-org/ledger
owner: time-pagamentos
status: active
trust: canonical
sources:
  - kind: code
    ref: ledger:src/ledger_service.py#LedgerService.post
relations:
  partOf: [examples/payments/index.md]
---
## Responsabilidade
Toda movimentação gera dois lançamentos (débito e crédito) que somam zero.

## Interfaces
- Entrada: evento `charge.completed`
- Saída: tabela `ledger_entries` (somente inserção)

## Armadilhas
- Nunca UPDATE/DELETE em `ledger_entries`; correção é um lançamento de estorno.
