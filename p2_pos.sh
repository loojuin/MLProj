#!/bin/bash

rm -f POS/dev.p2.out
python emission.py POS/train POS/dev.in POS/dev.p2.out
python comparator.py POS/dev.out POS/dev.p2.out
