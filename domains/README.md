# domains/

Um bundle OKF por domínio. Para criar um:

1. Copie a estrutura de [`examples/payments/`](../examples/payments/) para `domains/<dominio>/`.
2. Ajuste `index.md` (título, descrição, `owner`) e zere o `log.md`.
3. Troque os caminhos `examples/payments/` por `domains/<dominio>/` nas relações.
4. Adicione o domínio ao [`org/index.md`](../org/index.md) e ao `CODEOWNERS`.
5. Escreva as primeiras perguntas em `evals/` (ver [spec/05](../spec/05-evals.md)).
