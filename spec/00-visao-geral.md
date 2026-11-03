# 00 · Visão geral

> Especificação v0.3 · 2026-11-02 · só OKF, sem campos próprios · alinhada à [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)

## Problema

O conhecimento do time está espalhado em código, PRs, Jira, reuniões, Slack e na cabeça das pessoas. Os agentes de código começam cada sessão sem esse contexto, gastam a maior parte do tempo procurando e repetem erros que o time já resolveu. Wikis tradicionais não resolvem: envelhecem, ninguém confia nelas e agentes não as leem.

## Decisão de arquitetura

Duas camadas, cada uma com um padrão aberto:

| Camada | Onde | Padrão | Papel | Carregamento |
|---|---|---|---|---|
| **Instrução local** | Cada repo de projeto | [AGENTS.md](https://agents.md) | *Como trabalhar aqui*: comandos, arquivos-chave, armadilhas, limites | Automático, por toda ferramenta |
| **Conhecimento compartilhado** | Este repo, bundle `knowledge/` com um diretório por domínio | [Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) sem campos próprios | *O que é verdade*: decisões, regras, termos, serviços, runbooks, incidentes | Sob demanda (link, MCP, plugin) |

A ponte entre as duas é uma linha no `AGENTS.md` de cada repo apontando para o `index.md` do domínio a que ele pertence.

Ver a decisão completa em [knowledge/org/decisions/0001-agents-md-e-okf.md](../knowledge/org/decisions/0001-agents-md-e-okf.md) (em `draft`, aguardando revisão humana).

## Princípios

1. **Bússola, não enciclopédia.** Escreva só o que não dá para deduzir do código.
2. **Sem fonte, não é memória.** Toda afirmação cita de onde veio.
3. **Perto do código ganha de longe do código.** Instrução local vai no `AGENTS.md`; conhecimento que cruza repos vai no bundle.
4. **Substitua, não sobrescreva.** Decisões mudam por substituição; o histórico fica.
5. **Delta, não reescrita.** Agentes propõem mudanças pontuais, nunca reescrevem uma nota inteira.
6. **Domínio, não organograma.** Bundles são por domínio; o time dono é um campo.
7. **Memória sem dono apodrece.** Toda pasta tem dono no `CODEOWNERS`.
8. **Se não tem eval, não sabemos se ajuda.** Acurácia é medida.

## Estrutura deste repositório

```
agents-memory/
├── AGENTS.md / CLAUDE.md     # como agentes trabalham NESTE repo
├── spec/                     # esta especificação
├── schema/ontology.yaml      # tipos, seções e regras de humano (fonte do validador)
├── templates/                # AGENTS.md de projeto + um template por tipo de conceito
├── knowledge/                # bundle OKF v0.2 (index.md raiz com okf_version)
│   ├── org/                  #   padrões, termos e decisões transversais
│   └── domains/<dominio>/    #   um diretório por domínio
├── examples/payments/        # bundle de exemplo completo (referência)
├── graph/                    # GERADO sob demanda, não versionado (.gitignore)
├── tools/                    # validate.py, build_graph.py, ci.sh
├── CODEOWNERS                # dono de cada pasta (GitHub e GitLab)
├── .github/workflows/        # CI no GitHub (chama tools/ci.sh)
└── .gitlab-ci.yml            # CI no GitLab (chama tools/ci.sh)
```

## Índice da especificação

> **Terminologia:** "PR" nesta especificação é o pedido de mudança da forja: *pull request* no GitHub, *merge request* (MR) no GitLab.

| # | Documento | Conteúdo |
|---|---|---|
| 01 | [AGENTS.md](01-agents-md.md) | Padrão para repos de projeto |
| 02 | [Formato](02-formato.md) | OKF v0.2: frontmatter, fontes, links, bundles, `index.md`, `log.md` |
| 03 | [Tipos](03-tipos.md) | Cada tipo de conceito, campos e seções obrigatórias |
| 04 | [Ciclo de vida](04-ciclo-de-vida.md) | Captura → verificação → manutenção → `stale_after`; níveis de confiança da OKF; quando exigir humano |
| 05 | [Evals](05-evals.md) | Como medir acurácia (3 níveis) |
| 06 | [Grafo e acesso](06-grafo-e-acesso.md) | Grafo gerado, MCP, canais de entrega |
| 07 | [Governança](07-governanca.md) | Segurança, PII, o que exige humano |
| 08 | [Adoção](08-adocao.md) | Piloto, métricas, critérios de parada |
| 09 | [Forjas](09-forjas.md) | GitHub e GitLab: o que é igual, o que muda, aprovação obrigatória |

## Referências que embasam este desenho

- AGENTS.md — padrão aberto, arquivos aninhados por pasta: https://agents.md
- OKF v0.2 (Google Cloud, jul/2026): https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- Meta — contexto curto, verificado e auto-reparado: https://engineering.fb.com/2026/04/06/developer-tools/how-meta-used-ai-to-map-tribal-knowledge-in-large-scale-data-pipelines
- GitHub Copilot Memory — citações verificadas no uso, expiração: https://github.blog/ai-and-ml/github-copilot/building-an-agentic-memory-system-for-github-copilot
- Estudo ETH sobre AGENTS.md (ajuda o que não é dedutível do código; arquivo gerado sem curadoria atrapalha): https://arxiv.org/html/2602.11988v1
- Anthropic — CLAUDE.md por time, atualizado no review: https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf
