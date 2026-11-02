# 00 · Visão geral

> Especificação v0.1 · 2026-11-02

## Problema

O conhecimento do time está espalhado em código, PRs, Jira, reuniões, Slack e na cabeça das pessoas. Os agentes de código começam cada sessão sem esse contexto, gastam a maior parte do tempo procurando e repetem erros que o time já resolveu. Wikis tradicionais não resolvem: envelhecem, ninguém confia nelas e agentes não as leem.

## Decisão de arquitetura

Duas camadas, cada uma com um padrão aberto:

| Camada | Onde | Padrão | Papel | Carregamento |
|---|---|---|---|---|
| **Instrução local** | Cada repo de projeto | [AGENTS.md](https://agents.md) | *Como trabalhar aqui*: comandos, arquivos-chave, armadilhas, limites | Automático, por toda ferramenta |
| **Conhecimento compartilhado** | Este repo, um bundle por domínio | [Open Knowledge Format (OKF) v0.1](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) + extensões | *O que é verdade*: decisões, regras, termos, serviços, runbooks, incidentes | Sob demanda (link, MCP, plugin) |

A ponte entre as duas é uma linha no `AGENTS.md` de cada repo apontando para o `index.md` do domínio a que ele pertence.

Ver a decisão completa em [org/decisions/0001-agents-md-e-okf.md](../org/decisions/0001-agents-md-e-okf.md).

## Princípios

1. **Bússola, não enciclopédia.** Escreva só o que não dá para deduzir do código.
2. **Sem fonte, não é memória.** Toda afirmação cita de onde veio.
3. **Perto do código ganha de longe do código.** Instrução local vai no `AGENTS.md`; conhecimento que cruza repos vai no bundle.
4. **Substitua, não sobrescreva.** Decisões mudam por substituição; o histórico fica.
5. **Delta, não reescrita.** Agentes propõem mudanças pontuais, nunca reescrevem uma nota inteira.
6. **Domínio, não organograma.** Bundles são por domínio; o time dono é um campo.
7. **Memória sem dono apodrece.** Todo conceito tem `owner`.
8. **Se não tem eval, não sabemos se ajuda.** Acurácia é medida.

## Estrutura deste repositório

```
agents-memory/
├── AGENTS.md / CLAUDE.md     # como agentes trabalham NESTE repo
├── spec/                     # esta especificação
├── schema/ontology.yaml      # tipos e relações permitidos (fonte do validador)
├── templates/                # AGENTS.md de projeto + um template por tipo de conceito
├── org/                      # bundle da empresa (padrões, termos e decisões transversais)
├── domains/<dominio>/        # um bundle OKF por domínio
├── examples/payments/        # domínio de exemplo completo (referência)
├── graph/                    # GERADO: grafo, backlinks, Mermaid
└── tools/                    # validate.py, build_graph.py
```

## Índice da especificação

| # | Documento | Conteúdo |
|---|---|---|
| 01 | [AGENTS.md](01-agents-md.md) | Padrão para repos de projeto |
| 02 | [Formato](02-formato.md) | OKF + extensões: frontmatter, relações, bundles, `index.md`, `log.md` |
| 03 | [Tipos](03-tipos.md) | Cada tipo de conceito, campos e seções obrigatórias |
| 04 | [Ciclo de vida](04-ciclo-de-vida.md) | Captura → verificação → merge → manutenção → expiração; níveis de confiança |
| 05 | [Evals](05-evals.md) | Como medir acurácia (3 níveis) |
| 06 | [Grafo e acesso](06-grafo-e-acesso.md) | Grafo gerado, MCP, canais de entrega |
| 07 | [Governança](07-governanca.md) | Segurança, PII, o que exige humano |
| 08 | [Adoção](08-adocao.md) | Piloto, métricas, critérios de parada |

## Referências que embasam este desenho

- AGENTS.md — padrão aberto, arquivos aninhados por pasta: https://agents.md
- OKF v0.1 (Google Cloud, jun/2026): https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- Vocabulário de relações do Backstage: https://backstage.io/docs/features/software-catalog/well-known-relations
- Meta — contexto curto, verificado e auto-reparado: https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines
- GitHub Copilot Memory — citações verificadas no uso, expiração: https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot
- Estudo ETH sobre AGENTS.md (humano ajuda, gerado por LLM atrapalha): https://arxiv.org/html/2602.11988v1
- Anthropic — CLAUDE.md por time, atualizado no review: https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf
