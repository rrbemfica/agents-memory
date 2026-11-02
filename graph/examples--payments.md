# Grafo · examples/payments

> Gerado por `tools/build_graph.py`. Não edite à mão. Tracejado = não verificado · esmaecido = deprecated.

```mermaid
graph LR
  classDef unverified stroke-dasharray: 5 5
  classDef deprecated opacity:0.5
  n0{{"ADR-0031: Parcelamento financiado pela própria empresa"}}
  class n0 deprecated
  n1{{"ADR-0042: Idempotency-key obrigatória em chamadas a adquirentes"}}
  n2{{"ADR-0057: Pix parcelado com mínimo de R$ 100"}}
  n3>"2026-10-14: Timeout na Cielo derrubou cobranças de cartão"]
  n4["Produto Pagamentos, semana 44/2026"]
  n5["Idempotency-key obrigatória em chamadas a adquirentes"]
  n6["Pix parcelado exige valor mínimo de R$ 100"]
  n7["Rollback de cobranças Pix"]
  n8[("Cielo (adquirente)")]
  n9[("ledger")]
  n10[("payments-api")]
  n11("Chargeback")
  n12("Estorno")
  n13("Pix parcelado")
  class n13 unverified
  n1 -- decidesAbout --> n5
  n1 -- decidesAbout --> n10
  n2 -- decidesAbout --> n6
  n2 -- supersedes --> n0
  n2 -- usesTerm --> n13
  n3 -- causedBy --> n8
  n3 -- produced --> n7
  n4 -- produced --> n2
  n4 -- produced --> n13
  n6 -- usesTerm --> n13
  n7 -- usesTerm --> n12
  n10 -- dependsOn --> n8
  n10 -- dependsOn --> n9
  n10 -- implements --> n5
  n10 -- implements --> n6
```
