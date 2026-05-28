#!/usr/bin/env bash
# Simple wrapper

set -euo pipefail

DIR=$(dirname "$0")
cd "$DIR/.."
exec uv run taiga-stats "$@"
