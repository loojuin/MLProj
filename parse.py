#!~/anaconda/bin/python
#
# This module contains the logic for parsing the provided text files, and
# creating the StateNode objects that are used for later stages of this program.
#
# Running this module from the command line would perform the parsing on the provided file,
# and output the parsed sequence to the console.


import sys
from classes import *


# Convert a text file into complete StateNode sequences
# (that include both the tags and the words, and also START and STOP).
#
# Params:
# path_to_file - A string containing the relative path to the file to be parsed.
#
# Returns:
# 1) A list of lists of StateNode objects, with each list corresponding
#    to one block (separated by a blank line) in the file.
# 2) A list of strings, representing the tags that were observed in the file.
def parse_xy(path_to_file):
    seqs = []
    tags = set([])
    stop = Stop()
    start = Start(stop)
    pointer = start
    f = open(path_to_file, "r")
    for line in f:
        if line == "\n" or line == "\r" or line == "\r\n":
            if pointer != start:
                seqs.append(start.to_list())
                stop = Stop()
                start = Start(stop)
                pointer = start
        else:
            linesplit = line.strip().split(" ")
            x = linesplit[0]
            y = linesplit[1]
            tags.add(y)
            new_x = Word(x)
            new_y = Tag(y, new_x, stop)
            pointer.next_tag = new_y
            pointer = new_y
    if pointer != start:
        seqs.append(start.to_list())
    return seqs, list(tags)


# Convert a text file into lists of Word objects.
#
# Params:
# path_to_file - A string containing the relative path to the file to be parsed.
#
# Returns:
# A list of lists of Word objects, with each list corresponding to one block
# (separated by a blank line) in the file.
def parse_x(path_to_file):
    seqs = []
    holder = []
    f = open(path_to_file, "r")
    for line in f:
        if line == "\n" or line == "\r" or line == "\r\n":
            if len(holder) > 0:
                seqs.append(holder)
                holder = []
        else:
            linesplit = line.strip().split(" ")
            x = linesplit[0]
            new_x = Word(x)
            holder.append(new_x)
    if len(holder) > 0:
        seqs.append(holder)
    return seqs


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Too few argument. Usage $ python parser.py [x|xy] path/to/your/file"
        quit(0)
    filepath = sys.argv[2]
    if sys.argv[1] == "xy":
        s, t = parse_xy(filepath)
        for i in s:
            for p in i:
                print p
            print ""
        print t
    elif sys.argv[1] == "x":
        s = parse_x(filepath)
        for i in s:
            for p in i:
                print p
            print ""
    else:
        print "Invalid mode. Usage: $ python parser.py [x|xy] path/to/your/file"

