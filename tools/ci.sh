#!/usr/bin/env sh
# Checagens do CI, iguais em qualquer forja. Os arquivos de CI (GitHub, GitLab) só chamam este script.
# Uso: tools/ci.sh [--strict]
set -eu
cd "$(dirname "$0")/.."

python tools/validate.py "$@"
python tools/build_graph.py
if ! git diff --exit-code -- graph/; then
  echo "ERRO graph/ desatualizado. Rode 'python tools/build_graph.py' e commite o resultado." >&2
  exit 1
fi
if [ -n "$(git status --porcelain -- graph/)" ]; then
  echo "ERRO graph/ tem arquivos novos não commitados. Rode 'python tools/build_graph.py' e commite o resultado." >&2
  exit 1
fi
