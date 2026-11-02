# 06 · Grafo e acesso

## Grafo gerado

O Markdown é a fonte de verdade; o grafo é um **índice gerado** (`tools/build_graph.py`) a partir de `relations` e dos links do corpo.

| Arquivo gerado | Conteúdo |
|---|---|
| `graph/graph.json` | Nós (id, tipo, título, status, trust, owner) e arestas tipadas |
| `graph/backlinks.json` | Para cada conceito, quem aponta para ele ("citado por") e as relações inversas |
| `graph/<bundle>.md` | Diagrama Mermaid por bundle (o GitHub renderiza) |

Regras:
- **Não edite `graph/` à mão.** O CI falha se o grafo commitado estiver desatualizado.
- Relações inversas (`hasPart`, `dependencyOf`, `supersededBy`, `implementedBy`…) existem só no grafo.

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
| `memory_get(id)` | ID do conceito | conteúdo + trust + backlinks |
| `memory_search(query, type?, domain?)` | texto | lista de IDs com título e descrição |
| `memory_neighbors(id, depth=1, relation?)` | ID | vizinhos tipados |
| `memory_impact(id)` | ID | tudo que depende transitivamente (inversos de `dependsOn`, `decidesAbout`, `implements`) |
| `memory_history(id)` | ID de Decision | cadeia de `supersedes` |
| `memory_propose(concept)` | conceito | abre PR com candidato (passa pelo [ciclo](04-ciclo-de-vida.md)) |

Implementação sugerida: ler `graph/graph.json` em memória (NetworkX) + busca textual (grep/ripgrep). Banco de grafos só se aparecer necessidade real: > ~5 mil conceitos, consultas temporais frequentes (→ Graphiti) ou muitos saltos concorrentes (→ Kùzu/Neo4j). Mesmo assim, o Markdown continua sendo a fonte.
