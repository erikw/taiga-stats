#!/usr/bin/env bash

log_gen() {
	echo "⚙️  Generating $@..."
}

README_IN=README.md.in
README_OUT=README.md
COMMANDS_MD=docs/commands.md
SEARCH="<insert-helptext-here>"

DIR=$(dirname "$0")
cd $DIR/..

log_gen $README_OUT
rm -f $README_OUT
help=$(bin/taiga-stats.sh --help)
while read line; do
	if [ "$line" = $SEARCH ]; then
		echo "$help" >> $README_OUT
	else
		echo "$line" >> $README_OUT
	fi
done < $README_IN


log_gen $COMMANDS_MD
cat << EOF > $COMMANDS_MD
# Commands
\`\`\`console
$help
\`\`\`

Full documentation at [github.com/erikw/taiga-stats](https://github.com/erikw/taiga-stats).
EOF

log_gen mkdocs
poetry run mkdocs build
