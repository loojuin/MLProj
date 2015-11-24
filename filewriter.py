#!~/anaconda/bin/python
#


from classes import *
import os


def write_file(seqs, filename):
    if os.path.isfile(filename):
        print "ABORT - File %s already exists."%(filename)
        quit(0)
    f = open(filename, "w")
    for seq in seqs:
        for node in seq:
            if isinstance(node, SpecialNode):
                continue
            f.write(node.to_file() + "\n")
        f.write("\n")
    f.close()
