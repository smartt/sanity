#!/bin/sh

for i in `ls *.py`; do python $i --test; done

