#!/usr/bin/env sh

readme_in=README.md.in
readme_out=README.md
search="<insert-helptext-here>"

rm $readme_out
help=$(./taiga-stats --help)
while read line; do
	if [ "$line" = $search ]; then
		echo "$help" >> $readme_out
	else
		echo "$line" >> $readme_out
	fi
done < $readme_in
