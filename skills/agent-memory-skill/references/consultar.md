# Consultar a memória

Só leitura. Antes, ache o repo de memória e o domínio, e atualize a cópia (SKILL.md).

## 1. Ler do mais barato ao mais caro

1. A porta de entrada: `knowledge/domains/<dominio>/index.md`, ou `knowledge/org/index.md` para o que vale para todos. Cada item tem título e descrição.
2. Os conceitos listados que tocam a pergunta. Siga os links de `# Relacionados` só quando precisar.
3. Se ainda faltar: `grep -ril "<termo>" knowledge/`. Inclua sinônimos; os de um termo ficam em `tags`.
4. O `log.md` da área (domínio ou `org/`), quando a pergunta for "o que mudou" ou "por que tiraram".

Não leia o bundle inteiro. Perguntas sobre **como a própria memória funciona** (campos, tipos, processo) têm resposta em `spec/` do repo de memória: cite de lá.

## 2. Pesar cada conceito antes de usar

A confiança é derivada do frontmatter (OKF §5.3), não declarada. Aplique a **primeira** linha que valer:

| O que o frontmatter diz | Como tratar |
|---|---|
| `status: deprecated` | Não use. Siga o link "Substituída por" em `# Relacionados` |
| `stale_after` no passado | Desatualizado: trate com desconfiança e avise |
| `status: draft` | Proposta, não verdade. Diga que é proposta, e diga também o nível de confiança |
| `verified` com algum `by: human:…` | Revisado por humano: pode seguir como regra |
| `verified` só com `process:` ou agentes | Confirmado por máquina: use, e confira a fonte se o risco for alto |
| Sem `verified` | Não verificado: é pista. Confira a fonte antes de agir |

**Conferir a fonte:** comece pelas notas de rodapé (`[^id]: Título: "trecho"`), que trazem o trecho literal. Depois abra `sources[].resource` se der. Se a fonte não está ao seu alcance (URL externa, sistema fechado), diga que não conferiu.

## 3. Responder

- Responda a pergunta primeiro, depois as evidências.
- Para cada afirmação, cite o conceito (caminho do arquivo) e diga o nível de confiança quando não for "revisado por humano".
- Se a memória não responde, diga isso claramente. Não complete com suposição apresentada como memória.
- Se o código ou outra fonte contradiz um conceito, mostre a contradição.

## 4. Depois (oferecer, não fazer)

- **Contradição ou lacuna** confirmada pelo usuário: ofereça registrar a correção ou o conceito novo ([registrar.md](registrar.md)).
- **Você conferiu um conceito não verificado contra a fonte e ele bate:** ofereça acrescentar em `verified` um item com o seu próprio ator (`<ferramenta>/<modelo>`), também via [registrar.md](registrar.md).
