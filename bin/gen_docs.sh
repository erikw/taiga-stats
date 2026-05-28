#!/usr/bin/env bash

set -euo pipefail

log_gen() {
    echo "⚙️ Generating $*..."
}

README_IN=README.md.in
README_OUT=README.md
COMMANDS_MD=docs/commands.md
DOCS_REQUIREMENTS=docs/requirements.txt
SEARCH="<insert-helptext-here>"

DIR=$(dirname "$0")
cd "$DIR/.."

log_gen "$README_OUT"
rm -f "$README_OUT"
help=$(bin/taiga-stats.sh --help)
while IFS= read -r line; do
    if [ "$line" = "$SEARCH" ]; then
        printf '%s\n' "$help" >> "$README_OUT"
    else
        printf '%s\n' "$line" >> "$README_OUT"
    fi
done < "$README_IN"


log_gen "$COMMANDS_MD"
cat << EOF > "$COMMANDS_MD"
# Commands
\`\`\`console
$help
\`\`\`

Full documentation at [github.com/erikw/taiga-stats](https://github.com/erikw/taiga-stats).
EOF

log_gen "$DOCS_REQUIREMENTS"
uv export --frozen --only-group docs --no-default-groups --no-hashes --no-emit-project -o "$DOCS_REQUIREMENTS"

log_gen mkdocs
uv run --group docs mkdocs build
