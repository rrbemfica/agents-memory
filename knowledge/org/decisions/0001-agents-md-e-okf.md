---
type: Decision
title: "ADR-0001: AGENTS.md nos repos de projeto e bundles OKF v0.2 por domínio"
description: Instrução local em AGENTS.md; conhecimento compartilhado em bundles OKF v0.2 por domínio, com revisão humana só onde o risco pede.
tags: [memoria, padrao]
status: draft
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-02T23:55:00Z }
stale_after: 2026-12-02T00:00:00Z   # rascunho de agente: revisar até aqui
sources:
  - id: agents-md
    resource: https://agents.md
    title: AGENTS.md
  - id: okf-spec
    resource: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    title: Open Knowledge Format v0.2
    author: team:google-cloud-data-cloud
---
# Contexto
Agentes de código precisam de dois tipos de contexto: instruções sobre como trabalhar num repo e conhecimento do negócio e do time que atravessa vários repos. Um vault central único fica longe do código e não é lido automaticamente. Instruções só por repo não cobrem conhecimento de domínio.[^agents-md]

# Decisão
- Cada repo de projeto tem um `AGENTS.md` curto, escrito por pessoas, apontando para o seu domínio.
- O conhecimento compartilhado vive no bundle `knowledge/`, um diretório por domínio, no formato OKF v0.2.[^okf-spec] Usamos os campos do padrão para origem, confiança e frescor (`sources`, `generated`, `verified`, `status`, `stale_after`).
- Só OKF, sem campos próprios. Dono por pasta no `CODEOWNERS`; ligações como links no corpo, com o verbo no texto; trecho literal da fonte na nota de rodapé.
- Revisão humana é exigida para `Decision` estável, conteúdo de risco (segurança, compliance, dinheiro) e fonte externa. O resto entra sem verificação, com `stale_after`, e sobe de nível por evals e uso.
- A qualidade é medida por evals com resposta-ouro vinda da fonte.

# Alternativas rejeitadas
- Vault central único em Obsidian (modelo "Autonomous Engineering OS"): longe do código, links sem tipo, sem verificação.
- Só AGENTS.md: não cobre conhecimento que cruza repos e incha os arquivos.
- Wiki tradicional (Confluence, Notion): agentes não leem automaticamente; não tem fonte nem verificação.
- Revisão humana de tudo: vira fila e depois carimbo.
- Campos próprios de confiança e validade (`trust`, `expires`): a OKF v0.2 já os padroniza.
- Relações tipadas no frontmatter (`dependsOn`, `supersedes`…): resolvem consultas de impacto que ainda não temos, e leitores OKF as ignoram. Voltam por ADR se a necessidade aparecer.
- Banco de grafos desde o início: custo antes de provar valor; Markdown e um grafo gerado bastam.

# Consequências
- Dois lugares para manter, com regra clara do que vai em cada um (spec/01).
- A OKF ainda é jovem (v0.2) e pode mudar; o risco é baixo porque o formato é Markdown simples.
- Exige disciplina de fonte e um conjunto de evals por domínio.

# Revisitar quando
- A OKF publicar versão incompatível, ou as ferramentas passarem a ter memória de time nativa.
- O piloto não mostrar ganho mensurável nos evals (spec/08).

[^agents-md]: AGENTS.md: "The closest AGENTS.md to the edited file wins"
[^okf-spec]: Open Knowledge Format v0.2: "OKF v0.2 makes provenance, trust, lifecycle, and attestation first-class"
