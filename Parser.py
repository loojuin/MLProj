#!~/anaconda/bin/python
#


import sys
from classes import *


class XYParse(SeqContainer):
    def __init__(self, path_to_file):
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
                new_x = X(x)
                new_y = Y(y, new_x, stop)
                pointer.next_y = new_y
                pointer = new_y
        if pointer != start:
            seqs.append(start.to_list())
        self.seqs = seqs
        self.tags = tags


class XParse(SeqContainer):
    def __init__(self, path_to_file):
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
                new_x = X(x)
                holder.append(new_x)
        if len(holder) > 0:
            seqs.append(holder)
        self.seqs = seqs


if __name__ == "__main__":
    filepath = sys.argv[2]
    if sys.argv[1] == "xy":
        p = XYParse(filepath)
        s = p.seqs
        t = p.tags
        for i in s:
            for p in i:
                print p
            print ""
        print t
    elif sys.argv[1] == "x":
        p = XParse(filepath)
        s = p.seqs
        for i in s:
            for p in i:
                print p
            print ""
    else:
        print "Invalid mode. Usage: $ python parser.py [x|xy] path/to/your/file"

