#!/usr/bin/env sh

readme_in=README.md.in
readme_out=README.md
search="<insert-helptext-here>"

DIR=$(dirname "$0")
cd $DIR/..

rm $readme_out
help=$(bin/taiga_stats.sh --help)
while read line; do
	if [ "$line" = $search ]; then
		echo "$help" >> $readme_out
	else
		echo "$line" >> $readme_out
	fi
done < $readme_in
