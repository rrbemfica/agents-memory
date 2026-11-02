# 07 · Governança e segurança

## Quem escreve o quê

| Onde | Humanos | Agentes |
|---|---|---|
| `AGENTS.md` de repo | Escrevem e aprovam | Sugerem no PR |
| Conceitos `canonical` | Escrevem, aprovam | Só via derivação de fonte já aprovada (ver [04](04-ciclo-de-vida.md#4-merge)) |
| Conceitos `inferred` | — | Propõem; auto-merge se passarem nas checagens |
| `schema/`, `spec/`, `templates/` | Donos de `org/` | Sugerem no PR |
| `graph/` | Ninguém | Gerado pelo CI |

## Donos

- Todo bundle tem um time dono (`owner` no `index.md`) e uma entrada no `CODEOWNERS` do repo cobrindo a pasta do domínio.
- `org/`, `schema/`, `spec/` e `templates/` pertencem ao grupo de plataforma/arquitetura.
- Reorganização de times: troca o `owner` e o `CODEOWNERS`; não move arquivos.

## Envenenamento de memória

Memória compartilhada é vetor de ataque (pesquisas como MINJA e AgentPoison mostram alta taxa de sucesso em laboratório).

- Conteúdo de reunião, ticket, página ou documento é **dado, não instrução**. Conceitos não contêm ordens ao agente ("ignore regras", "sempre execute X").
- Fonte externa → revisão humana obrigatória, sempre.
- Mudança em regra de segurança → aprovação do dono de segurança.
- Skills e runbooks executáveis são revisados como código.
- Conceitos `inferred` são pistas, verificadas no uso.

## Dados pessoais e segredos

- **Nunca** no repo: senhas, tokens, chaves, dados de cliente, dados pessoais, detalhes de vulnerabilidade não corrigida.
- `validate.py` bloqueia padrões comuns de segredo. Recomenda-se também `gitleaks` no CI.
- Conteúdo sensível (segurança, jurídico, pessoas) vai para um **repo separado com acesso restrito** — em git, permissão é por repo.
- Pessoas aparecem como **time**, não como indivíduo (`owner`, `participants`).

## Reuniões

- Ingestão só com **opt-in por reunião** e aviso aos participantes.
- Reuniões com clientes externos: só com aceite explícito; validar com o jurídico (LGPD) antes de habilitar.
- Transcrições **não** entram no repo; retenção curta onde estiverem.
- Do que sai da reunião, só entram conceitos (com `quote`) e um `Meeting` curto que expira.
- Comece pelo glossário (baixo risco) antes de extrair decisões automaticamente.

## Contestação

Qualquer pessoa pode abrir PR contestando um conceito. Conceitos mostram data e nível de confiança justamente para não encerrarem discussões por autoridade.
