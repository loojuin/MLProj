#!/bin/bash

rm -f NPC/dev.p3.out
python viterbi.py NPC/train NPC/dev.in NPC/dev.p3.out
python comparator.py NPC/dev.out NPC/dev.p3.out
