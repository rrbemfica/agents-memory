# Criar um domínio

Um domínio é um diretório em `knowledge/domains/<dominio>/`, dentro do bundle OKF `knowledge/`. É organizado por domínio de negócio, não por time, porque times mudam. Os arquivos nascem dos templates; `examples/payments/` mostra um domínio completo como referência.

## 1. Perguntar ao usuário

- **Slug** do domínio, em `kebab-case` e sem acentos (ex.: `pagamentos`). Confira em `knowledge/domains/` que ainda não existe.
- **Nome de exibição**, com acentos (ex.: `Pagamentos`).
- **Time dono**, como a forja escreve, com `@` (`@grupo/time` ou `@usuario`).
- **Repos de projeto** do domínio: URL e uma linha sobre cada um.
- Uma frase sobre o que o domínio cobre.

Depois, prepare um branch `memoria/novo-dominio-<slug>` (SKILL.md).

## 2. Criar os arquivos

`knowledge/domains/<slug>/index.md`, a partir de `templates/concepts/domain-index.md`:
- **Sem frontmatter** (OKF §8).
- `# <Nome>`, a frase de escopo como parágrafo e a lista de repos (`* [Repo <nome>](<URL>) - <uma linha>`).
- Deixe só as seções que já têm itens. As outras entram junto com o primeiro conceito de cada tipo.

`knowledge/domains/<slug>/log.md`, a partir de `templates/concepts/domain-log.md`:

```markdown
# Log · <Nome>

## <hoje>
* **Criação**: domínio criado.
```

Não crie pastas vazias (o git não as guarda). Cada pasta de tipo nasce com o primeiro conceito.

## 3. Ligar o domínio ao resto

- `knowledge/domains/index.md`: acrescente `* [<Nome>](<slug>/) - <frase de escopo>` antes da linha do exemplo, que continua lá.
- `CODEOWNERS`: no fim, acrescente `/knowledge/domains/<slug>/  <time dono>`, sem realinhar as outras linhas. O time dono já vem com `@`. Use só a sintaxe comum a GitHub e GitLab, sem `[Seções]`.
- `knowledge/log.md`: no topo, sob `## <hoje>` (crie o título se não existir), `* **Criação**: domínio [<Nome>](domains/<slug>/).`

## 4. Pedir aprovação

"Pedir aprovação" no SKILL.md, com a mensagem `memoria(<slug>): cria o domínio` e este corpo:

```markdown
## O que muda
- Cria o domínio <Nome> em `knowledge/domains/<slug>/` (index.md e log.md)
- Dono no CODEOWNERS: <time dono>
- Listado em `knowledge/domains/index.md`

## Para quem revisa
- O nome e o escopo representam o domínio?
- O time dono está certo?
```

## 5. Sugerir os próximos passos

Do piloto em `spec/08-adocao.md`. Cada um vai num branch próprio, depois que o domínio for aceito (ou empilhado sobre o branch do domínio, avisando no PR/MR):
1. `AGENTS.md` nos 2 ou 3 repos mais ativos, com a linha `Domínio:` apontando para o novo `index.md` ([agents-md.md](agents-md.md)).
2. Cerca de 20 perguntas reais do time (Slack, onboarding, reviews) em `knowledge/domains/<slug>/evals/basico.yaml`, a partir de `templates/concepts/eval.yaml`.
3. Semear uns 20 conceitos que respondem a essas perguntas: os ADRs mais discutidos, termos que confundem, regras que já causaram bug ([registrar.md](registrar.md)). Semeie pelas dúvidas, não por completude.
