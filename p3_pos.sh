#!/bin/bash

rm -f POS/dev.p3.out
python viterbi.py POS/train POS/dev.in POS/dev.p3.out
python comparator.py POS/dev.out POS/dev.p3.out
