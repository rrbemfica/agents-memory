# Fechar a sessão

Objetivo: não perder o que custou caro descobrir, sem encher a memória de ruído. **Proponha; o usuário escolhe; nada é escrito sem o OK dele.**

## 1. Levantar candidatos

Releia a sessão: a conversa, o diff (`git diff`, `git log` da sessão), comandos que falharam e por quê, perguntas que o usuário precisou responder.

Procure:
- **Decisão tomada** com alternativas descartadas.
- **Regra de negócio** que o código aplica mas não explica.
- **Termo** que causou confusão ou tem sentido próprio no domínio.
- **Armadilha** que causou erro ou retrabalho.
- **Procedimento** que precisou ser descoberto (como rodar, como recuperar).
- **Fato sobre um serviço** (dependência, contrato, limite) que não está no código deste repo.

## 2. Filtrar

Descarte o que:
- se deduz lendo o código ou a documentação existente;
- só vale para esta tarefa;
- é preferência pessoal (vai em `~/.claude/CLAUDE.md` ou `CLAUDE.local.md`, não na memória do time);
- já está na memória. Confira com `grep -ril "<termo>" <repo de memória>/knowledge/`. Se o que está lá estiver errado ou incompleto, o candidato vira uma **atualização**.

Fique com no máximo **2** conceitos novos, descontando os já registrados nesta sessão. Prefira o que outra pessoa ou outro agente erraria sem saber.

## 3. Classificar o destino

| O candidato é… | Vai para | Procedimento |
|---|---|---|
| Instrução para trabalhar **neste repo** (comando, armadilha local, limite) | `AGENTS.md` do repo | [agents-md.md](agents-md.md) |
| Conhecimento do **domínio** (vale para vários repos ou para pessoas) | Conceito no bundle do domínio | [registrar.md](registrar.md) |
| Vale para **todos** os domínios | Conceito em `knowledge/org/` | [registrar.md](registrar.md) |

Cada fato fica em um lugar só. Se ele vai para a memória, o `AGENTS.md` pode só apontar para o conceito.

## 4. Propor ao usuário

Mostre uma tabela curta e pergunte quais registrar:

| # | Destino | Tipo | Título proposto | Fonte | Por que vale guardar |
|---|---|---|---|---|---|
| 1 | memória: pagamentos | Business Rule | … | PR #123, `src/x.ts#fn` | … |
| 2 | AGENTS.md | Armadilha | … | erro no teste … | … |

- A fonte precisa ser durável: commit, PR, issue, arquivo, ata. A conversa sozinha é fonte fraca; se for a única, diga isso.
- Diga o que vai pedir revisão humana (`Decision`, tags de risco, fonte externa).
- Se nada passou no filtro, diga "nada novo para registrar" e encerre. Não force.

## 5. Registrar o que o usuário escolher

- Conceitos: [registrar.md](registrar.md), um PR/MR com os conceitos escolhidos.
- Linhas de `AGENTS.md`: [agents-md.md](agents-md.md).
- No fim, liste o que foi proposto e os links dos PRs/MRs.
