# 01 · AGENTS.md nos repos de projeto

## O que é

Um README para agentes: instruções curtas sobre **como trabalhar naquele repo**. É padrão aberto ([agents.md](https://agents.md)) e é lido automaticamente por Codex, Copilot, Cursor e (via import) Claude Code.

## Regras

1. **Todo repo de projeto tem um `AGENTS.md` na raiz**, a partir do [template](../templates/AGENTS.md).
2. **Máximo de ~40 linhas por arquivo.** Passou disso, quebre por pasta ou mova o detalhe para um conceito no bundle.
3. **Agente escreve, pessoa aprova.** O normal é um agente propor o arquivo ou as linhas novas no PR, e uma pessoa do time aprovar no review. Quem aprova corta toda linha que não passa no [teste abaixo](#teste-para-cada-linha). O que piora o desempenho dos agentes não é o autor ser um LLM, e sim o arquivo repetir o que o agente descobriria sozinho.
4. **Uma linha de ponte** para o domínio: `Domínio: <nome> → <link para agents-memory/knowledge/domains/<nome>/index.md>`.
5. **`CLAUDE.md` contém apenas `@AGENTS.md`** (sem duplicar conteúdo).
6. **Arquivos aninhados** (`src/ledger/AGENTS.md`) só onde há regras realmente diferentes, e **o arquivo da raiz lista cada um** na seção "Regras por área" — nem toda ferramenta desce na árvore sozinha (o Codex só carrega da raiz até a pasta onde a sessão começou).
7. **Muda junto com o código.** PR que altera comando, arquivo-chave ou cria armadilha nova atualiza o `AGENTS.md` no mesmo PR.

## Seções

| Seção | Obrigatória | Conteúdo |
|---|---|---|
| Cabeçalho | Sim | Uma frase sobre o repo · `Domínio:` · `Dono:` |
| Comandos | Sim | Setup, rodar local, testes, lint, o que rodar antes do PR |
| Arquivos-chave | Sim | 3–6 pontos de entrada, com uma linha cada |
| Armadilhas não óbvias | Sim | O que já causou bug ou retrabalho e **não se deduz do código** |
| Não faça sem falar com o time | Recomendada | Limites de autonomia |
| Regras por área | Se houver aninhados | Lista dos `AGENTS.md` de subpastas |
| Veja também | Sim | Links para conceitos do bundle (ADRs, regras, termos) |

## Teste para cada linha

1. Um agente descobriria isso lendo o código em poucos minutos? → **não coloque**.
2. Isso já causou erro ou retrabalho? → **coloque**.
3. Vale só para uma pasta? → `AGENTS.md` da pasta.
4. É conhecimento de negócio/time, válido para vários repos? → **conceito no bundle**; aqui fica só o resumo de uma linha e o link.

## O que nunca vai no AGENTS.md

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
