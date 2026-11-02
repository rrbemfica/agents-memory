---
type: Domain
title: Pagamentos (exemplo)
description: Domínio FICTÍCIO de referência — cobranças com cartão e Pix, parcelamento e registro contábil.
owner: time-pagamentos
timestamp: 2026-11-02
tags: [exemplo]
---
> Este bundle é um **exemplo** para copiar. Nada aqui descreve sistemas reais.

## O que é
Recebe cobranças (cartão e Pix), envia aos adquirentes e registra cada movimentação no ledger contábil. Inclui o Pix parcelado.

## Serviços
- [payments-api](services/payments-api.md): entrada de toda cobrança
- [ledger](services/ledger.md): registro contábil de dupla entrada
- [Cielo](services/cielo.md): adquirente de cartão (externo)

## Decisões vigentes
- [ADR-0042](decisions/0042-idempotencia-adquirente.md): idempotency-key obrigatória em chamadas a adquirentes
- [ADR-0057](decisions/0057-pix-parcelado.md): Pix parcelado com mínimo de R$ 100 (substitui o [ADR-0031](decisions/0031-parcelamento-proprio.md))

## Regras de negócio
- [Pix parcelado exige mínimo de R$ 100](rules/pix-parcelado-minimo.md)
- [Idempotency-key obrigatória](rules/idempotency-key-obrigatoria.md)

## Termos-chave
- [Chargeback](terms/chargeback.md) · [Estorno](terms/estorno.md) · [Pix parcelado](terms/pix-parcelado.md)

## Runbooks
- [Rollback de cobranças Pix](runbooks/rollback-pix.md)

## Incidentes
- [2026-10-14: timeout na Cielo](incidents/2026-10-14-timeout-cielo.md)

## Repos
- payments-api: https://github.com/example-org/payments-api
- ledger: https://github.com/example-org/ledger
