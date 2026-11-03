#!/usr/bin/env sh
# Checagens do CI, iguais em qualquer forja. Os arquivos de CI (GitHub, GitLab) só chamam este script.
# Uso: tools/ci.sh [--strict]
set -eu
cd "$(dirname "$0")/.."

python tools/validate.py "$@"
# O grafo não é versionado: é gerado aqui só para o CI publicar como artefato.
python tools/build_graph.py
