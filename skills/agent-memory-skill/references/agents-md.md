# Escrever o AGENTS.md de um repo

O padrão [agents.md](https://agents.md) só define o arquivo: Markdown livre, na raiz, com aninhados permitidos. As seções são recomendação do time: `templates/AGENTS.md` e `spec/01-agents-md.md` no repo de memória. Se não houver acesso ao repo de memória, use a tabela do passo 2.

## 1. Levantar o que existe no repo de projeto

- **Instruções que já existem:** `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.cursor/rules/`, `.github/copilot-instructions.md`, `CONTRIBUTING.md`. Aproveite o que vale e proponha juntar tudo no `AGENTS.md`.
- **Comandos reais:** `package.json` (scripts), `Makefile`, `pyproject.toml`, `justfile`, configs de CI. Copie os comandos **com as flags** que o CI usa.
- **Confirme** os comandos baratos rodando-os (lint, um teste só). Se precisar instalar dependências ou usar a rede, peça antes. O que não deu para confirmar entra no arquivo e vai listado no PR/MR como "não verificado". Não invente comando: sem CI nem script que o mostre, pergunte ou deixe a linha de fora.
- **Armadilhas:** pergunte ao usuário o que já deu errado com agentes ou pessoas novas. Veja comentários `HACK`/`NOTE`/`IMPORTANT`, issues e reverts recentes (`git log -i --grep=revert`). Sem como perguntar, liste as perguntas no PR/MR.
- **Domínio:** em qual domínio da memória este repo fica (`knowledge/domains/index.md`)? Se ele ainda não existe nem está num PR/MR aberto, ofereça criá-lo antes ([new-domain.md](new-domain.md)). Se está num PR/MR aberto, escreva a linha com a URL que ele terá no `main` e diga no PR/MR que depende dele.

## 2. Escrever

Parta do template. Todas as seções são opcionais; **apague as que ficariam vazias**.

| Seção | Conteúdo |
|---|---|
| Cabeçalho | Uma frase sobre o repo, a linha `Domínio: <nome> → <URL>` e a linha da memória (abaixo). A URL é completa, montada a partir do `git remote get-url origin` do repo de memória: `https://<forja>/<grupo>/agents-memory/blob/main/knowledge/domains/<nome>/index.md` (no GitLab, `/-/blob/main/`). Sem `origin`, pergunte a URL ao usuário |
| Comandos | Setup, rodar local, testes com flags, um teste só, o que rodar antes do PR |
| Testes | Onde ficam, o que precisa de teste, o que não mockar |
| Estilo de código | Só o que o linter não pega, com um trecho curto de exemplo |
| Pontos de entrada | Arquivos por onde começar, só os não óbvios |
| Armadilhas | O que já causou bug ou retrabalho e não se deduz do código |
| Git e PR | Formato de commit e título, o que o PR precisa ter |
| Limites | **Sempre** · **Pergunte antes** · **Nunca** |
| Segurança | Segredos, dados sensíveis, o que não logar |
| Regras por área | Cada `AGENTS.md` aninhado: "Antes de mexer em `x/`, leia `x/AGENTS.md`" |
| Veja também | Links para conceitos do domínio (ADRs, regras) |

A linha da memória, logo abaixo de `Domínio:`, é o que faz os agentes usarem esta skill:

```markdown
Memória: se a tarefa toca regra de negócio, decisão ou integração do domínio, consulte com a skill `agent-memory-skill` antes de mudar; ao terminar, use-a para fechar a sessão.
```

Para cada linha, aplique o teste:
1. Um agente descobriria isso lendo o código em poucos minutos? **Corte.**
2. Já causou erro ou retrabalho? **Fica.**
3. Vale só para uma pasta? Vai no `AGENTS.md` da pasta.
4. É conhecimento do negócio, válido para vários repos? Vai para a memória ([record.md](record.md)); aqui fica uma linha com o link.
5. Já está num comentário do código, mas mudar aquilo é perigoso? Não repita o fato; um limite ("Pergunte antes de mudar `X`") pode ficar.

Evite: descrição da stack ou das pastas, conselhos genéricos, segredos, cópia do README.

## 3. Arquivos ao redor

- `CLAUDE.md` na raiz com só `@AGENTS.md`. Se já existe com conteúdo, proponha mover o conteúdo para o `AGENTS.md` e deixar só o import.
- `AGENTS.md` aninhado só onde as regras são realmente diferentes, sempre listado em "Regras por área" na raiz.

## 4. Pedir aprovação

Mostre o arquivo (ou o diff) e diga o que cortou e por quê. Com o OK do usuário, faça commit num branch do repo de projeto, seguindo a convenção de commit dele (sem convenção: `docs: AGENTS.md`), push e PR/MR, como em "Pedir aprovação" no SKILL.md, mas **sem** o validador, que é do repo de memória. Se o usuário pediu só os arquivos, mostre-os, pare antes do commit e diga na resposta o que ficou sem confirmação.

## Atualizar depois

Ao acrescentar uma linha (ex.: vinda do fechamento de sessão), edite só a seção certa, sem reescrever o arquivo, e aplique o teste à linha nova.
