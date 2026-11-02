---
type: Decision
title: "ADR-0001: AGENTS.md nos repos de projeto e bundles OKF por domínio"
description: Instrução local em AGENTS.md; conhecimento compartilhado em bundles OKF por domínio neste repo.
tags: [memoria, padrao]
timestamp: 2026-11-02
owner: plataforma
status: active
trust: canonical
sources:
  - kind: url
    ref: https://agents.md
    quote: "The closest AGENTS.md to the edited file wins"
  - kind: url
    ref: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
  - kind: doc
    ref: spec/00-visao-geral.md
relations:
  partOf: [org/index.md]
---
## Contexto
Agentes de código precisam de dois tipos de contexto: instruções sobre como trabalhar num repo, e conhecimento do negócio e do time que atravessa vários repos. Um vault central único fica longe do código e não é lido automaticamente; instruções só por repo não cobrem conhecimento de domínio.

## Decisão
- Cada repo de projeto tem um `AGENTS.md` curto, escrito por pessoas, apontando para o domínio a que pertence.
- O conhecimento compartilhado vive neste repo, um bundle por domínio, no formato Open Knowledge Format (OKF v0.1) com extensões para relações tipadas (vocabulário do Backstage onde houver), confiança, fonte e expiração.
- A qualidade é medida por evals com resposta-ouro vinda da fonte.

## Alternativas rejeitadas
- Vault central único em Obsidian (modelo "Autonomous Engineering OS"): longe do código, sem tipos de relação, sem verificação.
- Só AGENTS.md: não cobre conhecimento que cruza repos e incha os arquivos.
- Wiki tradicional (Confluence/Notion): agentes não leem automaticamente; sem fonte nem verificação.
- Banco de grafos desde o início: custo e complexidade antes de provar valor; Markdown + grafo gerado basta.

## Consequências
- Dois lugares para manter, com regra clara do que vai em cada um (spec/01).
- O OKF é v0.1 (rascunho) e pode mudar; o risco é baixo porque o formato é Markdown simples.
- Exige disciplina de fonte e um conjunto de evals por domínio.

## Revisitar quando
- O OKF publicar versão incompatível, ou surgir suporte nativo das ferramentas a memória de time.
- O piloto não mostrar ganho mensurável nos evals (spec/08).
