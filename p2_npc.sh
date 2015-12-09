#!/bin/bash

rm -f NPC/dev.p2.out
python emission.py NPC/train NPC/dev.in NPC/dev.p2.out
python comparator.py NPC/dev.out NPC/dev.p2.out
