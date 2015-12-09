#!~/anaconda/bin/python
#
# This module contains the logic for writing the StateNode sequences into text files.s


from classes import *
import os


def write_file(seqs, filename):
    if os.path.isfile(filename):
        raise Exception("File already exists: " + filename)
    f = open(filename, "w")
    for seq in seqs:
        for node in seq:
            if isinstance(node, SpecialNode):
                continue
            f.write(node.to_text() + "\n")
        f.write("\n")
    f.close()
