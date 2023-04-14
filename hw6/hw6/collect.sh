#!/bin/bash

mkdir gobmk
for value in {128,256,512,1024,2048}
do
	for i in {8,16,32,64,128,256}
	do
		python3 sim_424.py 445.gobmk.gz 16384 $i $value 1000 > gobmk/gobmk.$i.ways.$value.txt
	done
done
