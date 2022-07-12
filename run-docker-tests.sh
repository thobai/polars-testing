#!/bin/bash
START=1
END=8
 
for (( c=$START; c<=$END; c++ ))
do
    echo "Run with $c CPU(s)"
	docker run --cpus=$c polars_test
done