#!/bin/bash

rm -f POS/dev.p4.out
python kbest_viterbi.py 10 POS/train POS/dev.out POS/dev.p4.out
