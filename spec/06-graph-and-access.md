# 06 · Grafo e acesso

## Grafo gerado

O Markdown é a fonte de verdade; o grafo é um **índice gerado sob demanda e não versionado** (`tools/build_graph.py`) feito só com o que a OKF define: links do corpo (aresta `link`) e fontes internas em `sources[].resource` (aresta `source`). As arestas não têm tipo de negócio; o sentido está no texto da seção `# Relacionados` ([02](02-format.md#relações-entre-conceitos)).

| Arquivo gerado | Conteúdo |
|---|---|
| `graph/graph.json` | Nós (bundle, ID, tipo, título, status, nível de confiança, stale_after) e arestas |
| `graph/backlinks.json` | Para cada conceito, quem linka para ele (`linkedFrom`) e quem o usa como fonte (`citedBy`) |
| `graph/<bundle>--<area>.md` | Diagrama Mermaid por área (`org`, cada domínio). GitHub e GitLab renderizam. |

Regras:
- **`graph/` não é commitado** (está no `.gitignore`). Quem quiser o diagrama roda `python tools/build_graph.py`, ou baixa o artefato `grafo` da última pipeline.
- O MCP e o jardineiro, quando existirem, geram o grafo na hora, em memória, a partir do clone.
- Se um dia o grafo precisar ser versionado (consultas de impacto, histórico), isso volta por ADR.
- Os inversos (`linkedFrom`, `citedBy`) existem só no grafo.
- O dono de cada nó vem do `CODEOWNERS`, pela pasta.

## Canais de entrega

Uma fonte, vários canais. Nunca edite conhecimento direto num canal — eles são cópias.

| Quem | Canal | Como |
|---|---|---|
| Agente num repo de projeto | `AGENTS.md` | Linha `Domínio: …` aponta para o `index.md` |
| Agente de código (qualquer repo) | Plugin do time + MCP | [Skill](10-skills.md) `agent-memory-skill` e o servidor MCP abaixo |
| Pessoas não técnicas | Claude Project por domínio | Base de conhecimento sincronizada deste repo |
| Outras ferramentas (Cursor, Codex, ChatGPT) | MCP | Mesmo servidor |
| Humanos | GitHub ou GitLab | Leitura e PR/MR |

## Navegação por linha de comando (✅ implementada)

[`tools/memory.py`](../tools/memory.py) já faz as operações de leitura abaixo sobre o clone, montando o grafo em memória a cada chamada: `search`, `tree`, `read`, `neighbors`, `history` (e `domains`, `queue`). É o que a [skill](10-skills.md) usa. O CI roda a ferramenta em todo PR/MR para ela não quebrar em silêncio.

## Servidor MCP (📐 especificado, não implementado)

Ferramentas pequenas — agente recebe só o necessário.

| Ferramenta | Entrada | Saída |
|---|---|---|
| `memory_domain(name)` | nome do domínio | `index.md` + subgrafo de 1 salto |
| `memory_get(id)` | ID do conceito | conteúdo + nível de confiança + `stale_after` + backlinks |
| `memory_search(query, type?, domain?)` | texto | lista de IDs com título e descrição |
| `memory_neighbors(id, depth=1)` | ID | conceitos linkados e que linkam, com a linha de texto do link (onde está o verbo) |
| `memory_history(id)` | ID de Decision | cadeia de decisões ligadas por "Substitui" / "Substituída por" |
| `memory_propose(concept)` | conceito | abre PR com candidato (passa pelo [ciclo](04-lifecycle.md)) |

Implementação sugerida: um servidor fino sobre `tools/memory.py` (o grafo já é montado em memória por `memlib.edges`) + busca textual. Banco de grafos só se aparecer necessidade real: > ~5 mil conceitos, consultas temporais frequentes (→ Graphiti) ou muitos saltos concorrentes (→ Kùzu/Neo4j). Mesmo assim, o Markdown continua sendo a fonte.
