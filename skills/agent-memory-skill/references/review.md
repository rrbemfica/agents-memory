# Revisar a memória

Quem aprova é a **pessoa**. Você confere e prepara; ela decide. Você nunca:
- registra `verified` com `human:` sem que a própria pessoa, nesta conversa, confirme aquele conceito e diga o id dela;
- aprova nem faz merge do PR/MR na forja. Isso é com a pessoa.

Antes, ache o repo de memória e atualize a cópia (SKILL.md). Os comandos abaixo rodam da raiz do repo de memória.

## 1. Montar o que revisar

**Um PR/MR:** baixe e liste os arquivos.
- GitHub: `gh pr checkout <n>` e `gh pr diff <n> --name-only`
- GitLab: `glab mr checkout <n>` e `glab mr diff <n>`

**A fila** (revisão semanal):

```bash
python tools/memory.py queue [--domain <dominio>] [--days 14]
```

A fila olha o `main`. Para ver também o que espera revisão, liste os pedidos abertos: `gh pr list --search "memoria in:title"` ou `glab mr list --search memoria`.

A fila mostra drafts, não verificados, o que pede humano e `stale_after` vencido ou vencendo. Por padrão olha só o bundle `knowledge/`; `--all` inclui os exemplos.

## 2. Conferir cada conceito

1. **Validador:** `python tools/validate.py`. Erro = viola a OKF, precisa corrigir. Aviso = recomendação; anote os que tocam este conceito.
2. **Fontes:** abra cada `sources[].resource` (URL, arquivo do repo, outro conceito). Para cada nota de rodapé com trecho entre aspas, confirme que o trecho **existe literalmente** na fonte. Para cada afirmação, confirme que é o que a fonte diz. Se a fonte é outro conceito, confira nele; se o trecho não está lá, procure nas fontes dele (um nível) e sugira citar a fonte certa. Fonte fora do seu alcance: marque como não conferida. A pessoa decide se aprova mesmo assim.
3. **Duplicata ou conflito:** `python tools/memory.py search "<termos do título>"` e `neighbors <id>`. Conflito com conceito revisado por humano é decisão da pessoa.
4. **Revisão humana recomendada** (`spec/04-lifecycle.md`, "Quando pedir revisão humana"): `Decision` para virar `stable`, tags de `human_review_tags` da ontologia, fonte externa, descontinuar algo revisado por humano.
5. **Forma:** seções do tipo (`types.<Tipo>.sections`; seções a mais são permitidas), links com verbo em `# Relacionados` quando houver, entrada no `index.md` e no `log.md`.

## 3. Apresentar

Um bloco por conceito:

```markdown
### <caminho>  (<tipo>, <status>, <confiança>)
- Fontes: ✅ trechos conferidos | ⚠️ <trecho não encontrado em <fonte>>
- Conteúdo: <bate com a fonte | diverge em …>
- Conflitos: <nenhum | …>
- Validador: <avisos deste arquivo>
- Pede humano: <sim/não, por quê>
- Sugestão: <verificar | promover para stable | renovar | corrigir … | descontinuar | remover>
```

Depois pergunte o que a pessoa quer fazer com cada um. Para registrar `human:`, peça o id dela (o do `CODEOWNERS` sem `@`, ex.: `human:joana`). Se ela não é dona da pasta do conceito no `CODEOWNERS`, diga isso e sugira pedir ao dono; ela decide se segue.

## 4. Aplicar o que a pessoa aprovar

Edições pontuais, sem reescrever o conceito. O `log.md` e o `index.md` são os da área do conceito (o do domínio ou o de `org/`).

| Ação aprovada | No conceito | No `log.md` |
|---|---|---|
| Verificar | acrescente `- { by: human:<id>, at: <agora> }` à lista `verified` (crie a lista se não existir). `stale_after`: use o prazo "depois de verificado" de `spec/04`; onde é "sem `stale_after`" (ex.: `Decision`), tire o campo | **Verificação** |
| Promover | o mesmo, e `status: stable` (ou tire `status`); no `index.md`, tire da descrição menções a draft ou revisão pendente | **Verificação** |
| Renovar (vencido, ainda vale) | novo item em `verified` e novo `stale_after` | **Verificação** |
| Descontinuar | `status: deprecated` e "Substituída por […]" em `# Relacionados`, se houver substituto; tire das listas "vigentes" do `index.md` | **Descontinuação** |
| Remover (vencido, não vale mais) | apague o arquivo e a linha do `index.md`; corrija links que apontavam para ele | **Remoção** |
| Corrigir | edite só o trecho errado e mantenha o `generated` de quem escreveu | **Atualização** |

Depois, "Pedir aprovação" no SKILL.md, com uma diferença:
- Revisando um PR/MR: commit no branch do próprio pedido e push. A pessoa aprova e faz o merge na forja.
- Revisão da fila: branch `memoria/revisao-<dominio, org ou geral>-<hoje>` e PR/MR novo. Mensagem: `memoria(<dominio, org ou geral>): revisão de <hoje>`.
