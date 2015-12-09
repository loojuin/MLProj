#!/bin/bash

rm -f POS/dev.p5.out
python viterbi_opti.py POS/train POS/dev.in POS/dev.p5.out
python comparator.py POS/dev.out POS/dev.p5.out
