# 06 · Grafo e acesso

## Grafo gerado

O Markdown é a fonte de verdade; o grafo é um **índice gerado** (`tools/build_graph.py`) feito só com o que a OKF define: links do corpo (aresta `link`) e fontes internas em `sources[].resource` (aresta `source`). As arestas não têm tipo de negócio; o sentido está no texto da seção `# Relacionados` ([02](02-formato.md#relações-entre-conceitos)).

| Arquivo gerado | Conteúdo |
|---|---|
| `graph/graph.json` | Nós (bundle, ID, tipo, título, status, nível de confiança, stale_after) e arestas |
| `graph/backlinks.json` | Para cada conceito, quem linka para ele (`linkedFrom`) e quem o usa como fonte (`citedBy`) |
| `graph/<bundle>--<area>.md` | Diagrama Mermaid por área (`org`, cada domínio). O GitHub renderiza. |

Regras:
- **Não edite `graph/` à mão.** O CI falha se o grafo commitado estiver desatualizado.
- Os inversos (`linkedFrom`, `citedBy`) existem só no grafo.
- O dono de cada nó vem do `CODEOWNERS`, pela pasta.

## Canais de entrega

Uma fonte, vários canais. Nunca edite conhecimento direto num canal — eles são cópias.

| Quem | Canal | Como |
|---|---|---|
| Agente num repo de projeto | `AGENTS.md` | Linha `Domínio: …` aponta para o `index.md` |
| Agente de código (qualquer repo) | Plugin do time + MCP | Skills de consulta e o servidor MCP abaixo |
| Pessoas não técnicas | Claude Project por domínio | Base de conhecimento sincronizada deste repo |
| Outras ferramentas (Cursor, Codex, ChatGPT) | MCP | Mesmo servidor |
| Humanos | GitHub | Leitura e PR |

## Servidor MCP (📐 especificado, não implementado)

Ferramentas pequenas — agente recebe só o necessário.

| Ferramenta | Entrada | Saída |
|---|---|---|
| `memory_domain(name)` | nome do domínio | `index.md` + subgrafo de 1 salto |
| `memory_get(id)` | ID do conceito | conteúdo + nível de confiança + `stale_after` + backlinks |
| `memory_search(query, type?, domain?)` | texto | lista de IDs com título e descrição |
| `memory_neighbors(id, depth=1)` | ID | conceitos linkados e que linkam, com a linha de texto do link (onde está o verbo) |
| `memory_history(id)` | ID de Decision | cadeia de decisões ligadas por "Substitui" / "Substituída por" |
| `memory_propose(concept)` | conceito | abre PR com candidato (passa pelo [ciclo](04-ciclo-de-vida.md)) |

Implementação sugerida: ler `graph/graph.json` em memória (NetworkX) + busca textual (grep/ripgrep). Banco de grafos só se aparecer necessidade real: > ~5 mil conceitos, consultas temporais frequentes (→ Graphiti) ou muitos saltos concorrentes (→ Kùzu/Neo4j). Mesmo assim, o Markdown continua sendo a fonte.
