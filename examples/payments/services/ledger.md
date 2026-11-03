---
type: Service
title: ledger
description: Registro contábil de dupla entrada de todas as movimentações.
resource: https://github.com/example-org/ledger
tags: [contabil]
status: stable
generated: { by: human:tl-pagamentos, at: 2026-09-01T12:00:00Z }
verified: { by: human:tl-pagamentos, at: 2026-09-01T12:00:00Z }
stale_after: 2026-12-01T00:00:00Z
sources:
  - id: ledger-post
    resource: ledger:src/ledger_service.py#LedgerService.post
---
# Responsabilidade
Toda movimentação gera dois lançamentos (débito e crédito) que somam zero.[^ledger-post]

# Interfaces
- Entrada: evento `charge.completed`
- Saída: tabela `ledger_entries` (somente inserção)

# Armadilhas
- Nunca UPDATE ou DELETE em `ledger_entries`; correção é um lançamento de estorno.

[^ledger-post]: ledger, LedgerService.post
