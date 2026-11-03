# 09 · Forjas (GitHub e GitLab)

O núcleo não depende de forja: conceitos são Markdown com OKF, e `tools/validate.py` e `tools/build_graph.py` rodam sobre um clone git. O que muda de uma forja para outra são três peças finas, mantidas como adaptadores. O validador se comporta igual em qualquer forja: erro para o que viola a OKF ou vaza segredo, aviso para nossas recomendações.

## O que é igual

| Peça | Por quê |
|---|---|
| Conceitos, `index.md`, `log.md`, links relativos | Markdown comum; as duas forjas tratam `/` como raiz do repo, por isso usamos links relativos ([02](02-formato.md#identidade-e-links)) |
| Grafo como artefato | As duas publicam `graph/` como artefato da pipeline; o Mermaid renderiza nas duas |
| `sources[].resource` | `repo:caminho#símbolo` é neutro; URLs de qualquer forja valem |
| `AGENTS.md` dos repos de projeto | Aponta para o domínio por URL |
| Plugin de skills do time | Um marketplace de plugins pode ser qualquer URL git |

## O que muda

| Peça | GitHub | GitLab | Aqui |
|---|---|---|---|
| Donos | Lê `CODEOWNERS` na raiz, em `docs/` ou em `.github/` | Lê `CODEOWNERS` na raiz, em `docs/` ou em `.gitlab/` | [`CODEOWNERS`](../CODEOWNERS) **na raiz**, só com a sintaxe comum (`/caminho/ @dono`). Sem `[Seções]` do GitLab |
| CI | `.github/workflows/memory-ci.yml` | `.gitlab-ci.yml` | Os dois só chamam [`tools/ci.sh`](../tools/ci.sh) |
| Rodada semanal estrita | `schedule` no próprio workflow | Configurada na interface: *Build › Pipeline schedules* | Mesmo efeito: `tools/ci.sh --strict` |
| Pedido de mudança | Pull request (`gh`) | Merge request (`glab` ou API REST) | A spec diz "PR" para os dois. Automações usam uma interface de forja (abaixo) |

## Aprovação do dono

| Forja | `CODEOWNERS` pode bloquear o merge? |
|---|---|
| GitHub | Sim, com proteção de branch exigindo revisão de code owner (repos privados: GitHub Pro ou superior) |
| GitLab Premium/Ultimate | Sim, com a opção de aprovação de Code Owner no branch protegido |
| GitLab Free | **Não.** O arquivo só mostra quem é dono |

O validador, que roda igual em qualquer CI, só bloqueia o que viola a OKF e segredos (incluindo tokens do GitHub e do GitLab). As recomendações de revisão humana ([04](04-ciclo-de-vida.md#quando-pedir-revisão-humana)) aparecem como aviso no CI e são decididas pelo revisor do PR. Onde a forja permite, exigir aprovação do dono é a forma de garantir que alguém olhe esses avisos.

## Repos de projeto em outra forja

O repo de memória fica em **uma** forja só, a fonte de verdade. Repos de projeto na outra forja apontam para ele por URL no `AGENTS.md`; agentes e CI precisam de um token **só leitura**. Se precisar, use um espelho só leitura (pull mirroring do GitLab), sem nunca editar no espelho.

## Interface de forja para automações (📐 planejado)

As automações de [04](04-ciclo-de-vida.md) (fim de sessão, jardineiro) não chamam `gh` nem `glab` diretamente. Elas usam uma interface mínima, com uma implementação por forja escolhida por configuração:

| Operação | GitHub | GitLab |
|---|---|---|
| `abrir_pedido(branch, título, corpo)` | `gh pr create` | `glab mr create` |
| `comentar(pedido, texto)` | `gh pr comment` | `glab mr note` |
| `ler_arquivo(repo, caminho, ref)` | API de conteúdo | API de arquivos do repositório |
| `aprovacoes(pedido)` | API de reviews | API de approvals |

## Checklist para usar no GitLab

1. Importe ou espelhe o repo; `CODEOWNERS` e `.gitlab-ci.yml` já vêm prontos.
2. Troque os donos no `CODEOWNERS` por grupos do GitLab (`@grupo/subgrupo`).
3. Proteja o branch `main` (merge por mantenedores; no Premium, exija aprovação de Code Owner).
4. Crie o agendamento semanal em *Build › Pipeline schedules* (`0 6 * * 1`, branch `main`).
5. Se o projeto não for usar o GitHub, apague `.github/`.
