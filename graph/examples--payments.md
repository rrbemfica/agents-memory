# Grafo · examples/payments

> Gerado por `tools/build_graph.py`. Não edite à mão.

```mermaid
graph LR
  n0{{"ADR-0031: Parcelamento financiado pela própria empresa (superseded)"}}
  n1{{"ADR-0042: Idempotency-key obrigatória em chamadas a adquirentes"}}
  n2{{"ADR-0057: Pix parcelado com mínimo de R$ 100"}}
  n3>"2026-10-14: Timeout na Cielo derrubou cobranças de cartão"]
  n4(["Pagamentos (exemplo)"])
  n5["Produto Pagamentos, semana 44/2026"]
  n6["Idempotency-key obrigatória em chamadas a adquirentes"]
  n7["Pix parcelado exige valor mínimo de R$ 100"]
  n8["Rollback de cobranças Pix"]
  n9[("Cielo (adquirente)")]
  n10[("ledger")]
  n11[("payments-api")]
  n12("Chargeback")
  n13("Estorno")
  n14("Pix parcelado")
  n1 -- decidesAbout --> n6
  n1 -- decidesAbout --> n11
  n2 -- decidesAbout --> n7
  n2 -- supersedes --> n0
  n2 -- usesTerm --> n14
  n3 -- causedBy --> n9
  n3 -- produced --> n8
  n5 -- produced --> n2
  n5 -- produced --> n14
  n7 -- usesTerm --> n14
  n8 -- usesTerm --> n13
  n11 -- dependsOn --> n9
  n11 -- dependsOn --> n10
  n11 -- implements --> n6
  n11 -- implements --> n7
```
