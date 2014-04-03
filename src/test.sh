#!/bin/bash

set -e

rm -f output.txt

while read line
do
	num=$(( RANDOM % 10 ))
	if [[ $num -ne 0 ]]; then
		continue
	fi

	word="$line"
	echo "$word"
	echo "$word" >> output.txt

	./adbtwo.py -key AIzaSyD-DxMBEDLEzKmCW5yWoyJ8gbMUO0_bXuY -q "$word" -t infobox >> output.txt 2>&1

	echo "" >> output.txt
done < dictwords
