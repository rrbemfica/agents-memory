# <nome-do-repo>

<Uma frase: o que este repo faz.>
Domínio: <dominio> → <URL completa de agents-memory/knowledge/domains/<dominio>/index.md na forja>
Memória: se a tarefa toca regra de negócio, decisão ou integração do domínio, consulte com a skill `agent-memory-skill` antes de mudar; ao terminar, use-a para fechar a sessão.

<!-- Todas as seções são opcionais (spec/01). Apague as que não têm nada que o agente não descobriria sozinho. -->

## Comandos
- Setup: `<comando>`
- Rodar local: `<comando>`
- Testes: `<comando com flags>` · um teste só: `<comando>`
- Antes do PR: `<lint + testes>`

## Testes
- <onde ficam, o que precisa de teste, o que não mockar>

## Estilo de código
<!-- Só o que o linter não pega. Um exemplo curto vale mais que parágrafos. -->
```<linguagem>
<trecho curto mostrando o estilo esperado>
```

## Pontos de entrada
- `<caminho>`: <o que é, em uma linha>

## Armadilhas
<!-- Só o que já causou bug ou retrabalho e NÃO se deduz do código. Link para o conceito quando houver. -->
- <armadilha> (ver <ADR ou regra>)

## Git e PR
- Commit: <formato>
- PR: <título, o que precisa ter>

## Limites
- Sempre: <…>
- Pergunte antes: <…>
- Nunca: <…>

## Segurança
- <segredos, dados sensíveis, o que não logar>

## Regras por área
<!-- Liste cada AGENTS.md aninhado; apague a seção se não houver. -->
- Antes de mexer em `<pasta>/`, leia `<pasta>/AGENTS.md`

## Veja também
- [<ADR ou regra do domínio>](<link>)
