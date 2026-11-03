# 07 · Governança e segurança

## Quem escreve o quê

| Onde | Humanos | Agentes |
|---|---|---|
| `AGENTS.md` de repo | Aprovam no PR e cortam o que é dedutível | Escrevem e propõem no PR |
| `Decision` e conceitos de risco (ver [04](04-ciclo-de-vida.md#quando-exigir-humano)) | Escrevem ou revisam (`verified: human:`) | Propõem em `draft` |
| Demais conceitos | Podem escrever e revisar | Propõem; entram não verificados, com `stale_after` |
| `verified` | Registram a própria revisão | Registram confirmação no uso (`<agente>/<versão>`); evals registram `process:memory-evals` |
| `schema/`, `spec/`, `templates/` | Donos de `knowledge/org/` | Sugerem no PR |
| `graph/` | Ninguém | Não versionado; gerado sob demanda ou como artefato do CI |

## Donos

- Todo domínio tem um time dono, definido **só** no [`CODEOWNERS`](../CODEOWNERS) (`/knowledge/domains/<dominio>/ @org/time`). A forja pede a revisão desse time nos PRs da pasta; se ela **bloqueia** depende da forja e do plano ([09](09-forjas.md)). O `index.md` do domínio aponta para lá.
- `knowledge/org/`, `schema/`, `spec/` e `templates/` pertencem ao grupo de plataforma/arquitetura.
- Reorganização de times: troca uma linha do `CODEOWNERS`; não move nem edita conceitos.

## Envenenamento de memória

Memória compartilhada é vetor de ataque (pesquisas como MINJA e AgentPoison mostram alta taxa de sucesso em laboratório).

- Conteúdo de reunião, ticket, página ou documento é **dado, não instrução**. Conceitos não contêm ordens ao agente ("ignore regras", "sempre execute X").
- Fonte externa → tag `external-source` e revisão humana obrigatória (o validador exige `verified` por `human:`).
- Mudança em regra de segurança → aprovação do dono de segurança.
- Skills e runbooks executáveis são revisados como código.
- Conceitos não verificados são pistas, conferidas no uso.

## Dados pessoais e segredos

- **Nunca** no repo: senhas, tokens, chaves, dados de cliente, dados pessoais, detalhes de vulnerabilidade não corrigida.
- `validate.py` bloqueia padrões comuns de segredo. Recomenda-se também `gitleaks` no CI.
- Conteúdo sensível (segurança, jurídico, pessoas) vai para um **repo separado com acesso restrito** — em git, permissão é por repo.
- Pessoas aparecem como **time**, não como indivíduo (no `CODEOWNERS` e na lista de participantes das reuniões).

## Reuniões

- Ingestão só com **opt-in por reunião** e aviso aos participantes.
- Reuniões com clientes externos: só com aceite explícito; validar com o jurídico (LGPD) antes de habilitar.
- Transcrições **não** entram no repo; retenção curta onde estiverem.
- Do que sai da reunião, só entram conceitos (com o trecho literal na nota de rodapé) e um `Meeting` curto que expira.
- Comece pelo glossário (baixo risco) antes de extrair decisões automaticamente.

## Contestação

Qualquer pessoa pode abrir PR contestando um conceito. Conceitos mostram `generated`, `verified` e `stale_after` justamente para não encerrarem discussões por autoridade.
