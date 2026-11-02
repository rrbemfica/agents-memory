# 08 · Adoção

## Piloto (4 semanas, 1 domínio)

**Semana 1 — Fundação**
- [ ] Escolher o domínio piloto e o time dono.
- [ ] `AGENTS.md` escrito à mão nos 2–3 repos mais ativos do domínio (template em [`templates/AGENTS.md`](../templates/AGENTS.md)), com `CLAUDE.md` → `@AGENTS.md`.
- [ ] Criar `domains/<dominio>/` a partir de `examples/payments/`.
- [ ] 20 perguntas de eval a partir de dúvidas reais (Slack, onboarding, reviews).

**Semana 2 — Semear**
- [ ] ~20 conceitos respondendo às perguntas acima: os ADRs mais discutidos, termos que confundem, regras de negócio que já causaram bug, serviços do domínio.
- [ ] `index.md` do domínio completo.
- [ ] CI verde (`validate.py`, `build_graph.py`).

**Semanas 3–4 — Usar e medir**
- [ ] Hábito de fim de sessão: agente sugere no máximo 2 candidatos.
- [ ] Revisão semanal de 15 min do domínio (candidatos, conflitos, expirados).
- [ ] Rodar as perguntas de eval com e sem memória (manualmente, até o runner existir).

## Critérios (definidos antes de começar)

**Continua se:**
- acurácia com memória > sem memória nas perguntas de eval;
- candidatos revisados em menos de 7 dias;
- o time diz que usaria de novo.

**Para ou redesenha se:**
- não há ganho mensurável nos evals;
- fila de candidatos passa de 2 semanas;
- ninguém consulta nada além do `AGENTS.md`.

## Riscos conhecidos

| Risco | Sinal | Mitigação |
|---|---|---|
| Revisão vira gargalo ou carimbo | Fila envelhecendo, ou aceitação > 90% | Limite de candidatos, auto-merge para baixo risco, guardião rotativo |
| Agentes não consultam o bundle | Poucas leituras além do `AGENTS.md` | Linha de ponte no `AGENTS.md`, plugin/hook que injeta o `index.md` |
| Começo vazio → abandono | Perguntas sem resposta no bundle | Semear pelas dúvidas mais repetidas, não por completude |
| Memória errada que parece certa | Evals caindo, contradições no uso | Fonte por símbolo, reverificação quando a fonte muda, amostragem mensal |
| Duas fontes de verdade (AGENTS.md × bundle) | Contradições | Cada fato em um lugar; o outro só aponta |
| Expiração mata conhecimento raro | Conceito útil some | Prazos por tipo; `Incident` e `Decision` não expiram |
| "Já foi rejeitado" vira dogma | Discussões encerradas pelo ADR | Seção `Revisitar quando` |

## Depois do piloto

1. Servidor MCP de leitura.
2. Runner de evals (com/sem memória) no CI.
3. Gardener (reverificação quando a fonte muda, expiração).
4. Canais: plugin do time, Claude Project por domínio.
5. Segundo e terceiro domínios.
