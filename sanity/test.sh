#!/bin/sh

echo "Testing in Python 2.7..."
for i in `ls *.py`; do python2.7 $i --test; done

echo "Testing in Python 3.4..."
for i in `ls *.py`; do python3.4 $i --test; done
