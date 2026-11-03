---
okf_version: "0.2"
---
# Pagamentos (exemplo fictício)

* [Dono](../../CODEOWNERS) - pagamentos
* [Repo payments-api](https://github.com/example-org/payments-api) - entrada de cobranças
* [Repo ledger](https://github.com/example-org/ledger) - registro contábil

# Serviços

* [payments-api](services/payments-api.md) - recebe cobranças de cartão e Pix
* [ledger](services/ledger.md) - registro contábil de dupla entrada
* [Cielo](services/cielo.md) - adquirente de cartão (externo)

# Decisões vigentes

* [ADR-0042](decisions/0042-idempotencia-adquirente.md) - idempotency-key obrigatória em chamadas a adquirentes
* [ADR-0057](decisions/0057-pix-parcelado.md) - Pix parcelado com mínimo de R$ 100 (substitui o [ADR-0031](decisions/0031-parcelamento-proprio.md))

# Regras de negócio

* [Pix parcelado exige mínimo de R$ 100](rules/pix-parcelado-minimo.md) - cobranças abaixo disso não parcelam
* [Idempotency-key obrigatória](rules/idempotency-key-obrigatoria.md) - nenhuma chamada a adquirente sem chave

# Termos

* [Chargeback](terms/chargeback.md) - contestação pelo portador junto ao emissor
* [Estorno](terms/estorno.md) - devolução iniciada por nós
* [Pix parcelado](terms/pix-parcelado.md) - Pix financiado por parceiro e pago em parcelas

# Runbooks e incidentes

* [Reconciliar cobranças de cartão](runbooks/reconciliar-cartao-falha-adquirente.md) - quando o adquirente falha no meio da cobrança
* [2026-10-14: timeout na Cielo](incidents/2026-10-14-timeout-cielo.md) - pool esgotado no pico

# Reuniões

* [Produto, semana 44](meetings/2026-w44-produto.md) - definição do Pix parcelado
