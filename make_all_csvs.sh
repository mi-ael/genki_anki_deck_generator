#!/bin/sh
echo "this does not make the chapter 13 YAML template because that one
was modified by hand after being converted from CSV"
for l in wrk/csv/L* ; do
	echo "turn $l in YAML"
	./csv2yaml.py $l
done
