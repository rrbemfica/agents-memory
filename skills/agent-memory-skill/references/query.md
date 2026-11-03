# Consultar a memória

Só leitura. Antes, ache o repo de memória e o domínio, e atualize a cópia (SKILL.md). Os comandos rodam da raiz do repo de memória.

A navegação é **guiada**: uma ferramenta devolve listas curtas (id, tipo, título, confiança, descrição) e você abre só o que importa. Não use `cat` em pastas nem leia o bundle inteiro.

```bash
python tools/memory.py <comando> [--limit N]
```

| Comando | Para quê | Devolve |
|---|---|---|
| `domains` | Ver as áreas que existem | Cada área com o valor para `--domain`, a pasta e quantos conceitos tem |
| `tree <área ou pasta> [--depth 2]` | Descer a árvore | Pastas com contagem; no último nível, os conceitos com descrição |
| `search "termos" [--domain d] [--type T]` | Achar por assunto | Conceitos por quantos termos bateram (`[3/4 termos]`), com descrição e o trecho. Com `--domain`, inclui `org/` |
| `read <id> [--summary]` | Abrir um conceito | Confiança, autoria, fontes, corpo e as ligações (para onde liga e quem liga para ele, com a frase do link) |
| `neighbors <id> [--depth 2]` | Percorrer o grafo | Conceitos ligados, nos dois sentidos, com a frase onde está o verbo (`Depende de`, `Implementa`…) |
| `history <id>` | Cadeia de uma decisão | ADRs em ordem de data, com a frase de substituição e o vigente marcado |

`<id>` aceita o id completo, o caminho ou um começo único do nome (`0057`, `rules/pix-parcelado-minimo`). Por padrão só o bundle `knowledge/` aparece; para ver os exemplos fictícios, passe `--all` em **todos** os comandos.

## 1. Entrar

- **Sabe o assunto:** `search "<termos>" --domain <dominio>`, com o valor que `domains` mostra. Poucos termos específicos funcionam melhor que frases. Inclua sinônimos e o termo em inglês se o código usar. Resultado só com `[1/N termos]` é sinal fraco.
- **Não sabe por onde começar:** `tree knowledge/domains/<dominio>`, depois a pasta que interessa (`decisions`, `rules`…). O `index.md` do domínio é o índice curado: leia-o quando a árvore não bastar.
- **Vale para todos os domínios:** `org/` já entra em `search --domain`; para navegar, `tree knowledge/org`.
- **Pergunta sobre como a própria memória funciona** (campos, tipos, processo): a resposta está em `spec/` do repo de memória. Cite de lá.

## 2. Abrir e percorrer, com teto

1. `read <id> --summary` no candidato mais promissor. Se é ele, `read <id>` para o corpo.
2. Precisa do contexto? Siga as ligações que `read` mostrou, ou `neighbors <id>`. Para decisões, `history <id>`.
3. **Teto:** até **5 conceitos distintos** abertos com `read` por pergunta (`--summary` e a leitura completa do mesmo conceito contam como um). Pare assim que a pergunta estiver respondida. Chegou ao teto sem resposta? Diga ao usuário o que encontrou e o que falta, em vez de continuar lendo.

## 3. Pesar cada conceito antes de usar

`read` mostra a confiança, derivada do frontmatter (OKF §5.3). Aplique a **primeira** linha que valer:

| A confiança diz | Como tratar |
|---|---|
| `deprecated` | Não use. Siga a ligação "Substituída por" (`history <id>`) |
| `vencido desde …` | Desatualizado: trate com desconfiança e avise |
| `draft` | Proposta, não verdade. Diga que é proposta, e diga também o nível de confiança |
| `revisado por humano` | Pode seguir como regra |
| `confirmado por máquina` | Use, e confira a fonte se o risco for alto |
| `não verificado` | É pista. Confira a fonte antes de agir |

**Conferir a fonte:** comece pelas notas de rodapé no corpo (`[^id]: Título: "trecho"`), que trazem o trecho literal. Depois abra a fonte listada por `read`, se der. Se a fonte não está ao seu alcance (URL externa, sistema fechado), diga que não conferiu.

## 4. Responder

- Responda a pergunta primeiro, depois as evidências.
- Para cada afirmação, cite o id do conceito e diga o nível de confiança quando não for "revisado por humano".
- Se a memória não responde, diga isso claramente. Não complete com suposição apresentada como memória.
- Se o código ou outra fonte contradiz um conceito, mostre a contradição.

## 5. Depois (oferecer, não fazer)

- **Contradição ou lacuna** confirmada pelo usuário: ofereça registrar a correção ou o conceito novo ([record.md](record.md)).
- **Você conferiu um conceito não verificado contra a fonte e ele bate:** ofereça acrescentar em `verified` um item com o seu próprio ator (`<ferramenta>/<modelo>`), também via [record.md](record.md).
