#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="litestar-eval"
HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "${HERE}/.." && pwd)"

cd "${PROJECT_ROOT}"

echo "=== Building Docker image ==="
docker build -f .helix/Dockerfile.helix -t "${IMAGE_NAME}" .

if [ $# -eq 0 ]; then
    echo "=== Running all unit tests ==="
    docker run --rm "${IMAGE_NAME}" uv run pytest -x -v tests/unit/
else
    echo "=== Running tests: $* ==="
    docker run --rm "${IMAGE_NAME}" uv run pytest -x -v "$@"
fi
