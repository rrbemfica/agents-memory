# 01 · AGENTS.md nos repos de projeto

## O que é

Um README para agentes: instruções sobre **como trabalhar naquele repo**. É padrão aberto ([agents.md](https://agents.md)) e é lido automaticamente por Codex, Copilot, Cursor e (via import) Claude Code.

O padrão só define o arquivo: Markdown livre, na raiz, com arquivos aninhados permitidos (vale o mais próximo do arquivo editado). **Não exige nenhuma seção.** Tudo abaixo é **recomendação** nossa, baseada nas seções populares sugeridas pelo próprio [agents.md](https://agents.md), no [estudo do GitHub com mais de 2.500 repositórios](https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories) e no [estudo da ETH](https://arxiv.org/html/2602.11988v1).

## Recomendações

1. **Um `AGENTS.md` na raiz de cada repo de projeto**, partindo do [template](../templates/AGENTS.md).
2. **Agente escreve, pessoa aprova.** O normal é um agente propor o arquivo ou as linhas novas no PR, e uma pessoa do time aprovar no review. Quem aprova corta toda linha que não passa no [teste abaixo](#teste-para-cada-linha). O que piora o desempenho dos agentes não é o autor ser um LLM, e sim o arquivo repetir o que o agente descobriria sozinho.
3. **Duas linhas de ponte** para o domínio: `Domínio: <nome> → <URL do index.md do domínio>` e `Memória: …`, que diz ao agente para consultar com a [skill](10-skills.md) quando a tarefa toca regra de negócio, decisão ou integração, e para fechar a sessão com ela no fim. A skill não depende de gatilho automático para ser usada.
4. **`CLAUDE.md` contendo apenas `@AGENTS.md`**, para o Claude Code ler o mesmo arquivo sem duplicar conteúdo.
5. **Arquivos aninhados** (`src/ledger/AGENTS.md`) só onde há regras realmente diferentes, e **o arquivo da raiz lista cada um** na seção "Regras por área": nem toda ferramenta desce na árvore sozinha (o Codex só carrega da raiz até a pasta onde a sessão começou).
6. **Muda junto com o código.** PR que altera comando ou cria armadilha nova atualiza o `AGENTS.md` no mesmo PR.
7. **Comece pequeno e cresça com os erros.** Acrescente uma linha quando um agente errar algo que ela teria evitado.

## Seções recomendadas

Todas opcionais. Se uma seção não tem nada que o agente não descobriria sozinho, deixe de fora.

| Seção | Conteúdo | De onde vem |
|---|---|---|
| Cabeçalho | Uma frase sobre o repo · `Domínio:` · `Memória:` | agents.md (visão geral), em poucas linhas por causa da ETH |
| Comandos | Setup, rodar local, testes **com flags**, como rodar um teste só, o que rodar antes do PR. Logo no começo do arquivo | agents.md, GitHub |
| Testes | Onde ficam, o que precisa de teste, o que não mockar | agents.md, GitHub |
| Estilo de código | Só o que o linter não pega, com **um trecho curto de exemplo** | agents.md, GitHub |
| Pontos de entrada | Os arquivos por onde começar, só os que não são óbvios | GitHub (estrutura), filtrado pela ETH |
| Armadilhas | O que já causou bug ou retrabalho e **não se deduz do código** | nossa |
| Git e PR | Formato de commit e de título, o que o PR precisa ter | agents.md, GitHub |
| Limites | Três níveis: **Sempre** · **Pergunte antes** · **Nunca** | GitHub |
| Segurança | Segredos, dados sensíveis, o que não logar | agents.md |
| Regras por área | Lista dos `AGENTS.md` aninhados | nossa (contorna o limite do Codex) |
| Veja também | Links para conceitos do domínio (ADRs, regras, termos) | nossa |

## Teste para cada linha

1. Um agente descobriria isso lendo o código em poucos minutos? → **não coloque**.
2. Isso já causou erro ou retrabalho? → **coloque**.
3. Vale só para uma pasta? → `AGENTS.md` da pasta.
4. É conhecimento de negócio/time, válido para vários repos? → **conceito no bundle**; aqui fica só o resumo de uma linha e o link.

## O que evitar

- Descrição da stack, da estrutura de pastas ou da linguagem (o agente vê sozinho).
- Conselhos genéricos ("escreva código limpo").
- Segredos, tokens, dados de cliente.
- Conteúdo gerado automaticamente e aceito sem revisão: tende a repetir README e código. No estudo da ETH, arquivos assim pioraram o resultado em ~3% e custaram ~20% mais.

## Relação com o bundle

| Pergunta | Vai em |
|---|---|
| Muda o que o agente deve **fazer** neste repo? | `AGENTS.md` |
| Explica o que é **verdade** no negócio/time e vale para vários repos? | Conceito no bundle |
| Os dois | Conceito no bundle + uma linha de resumo com link no `AGENTS.md` |
