#!~/anaconda/bin/python
#


import sys


class XY:
    def __init__(self, x, y, parent = None):
        self.x = x
        self.y = y
        self.parent = parent

    def __repr__(self):
        parent_name = "NONE" if self.parent is None else self.parent.y
        return "(%s, %s) [%s]"%(self.x, self.y, parent_name)


class X:
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return self.x


def parse_xy(path_to_file):
    retval = []
    holder = []
    parent = None
    f = open(path_to_file, "r")
    for line in f:
        if line == "\n" or line == "\r" or line == "\r\n":
            if len(holder) > 0:
                retval.append(holder)
                holder = []
                parent = None
        else:
            linesplit = line.strip().split(" ")
            x = linesplit[0]
            y = linesplit[1]
            piece = XY(x, y, parent)
            parent = piece
            holder.append(piece)
    if len(holder) > 0:
        retval.append(holder)
    return retval


def parse_x(path_to_file):
    retval = []
    holder = []
    f = open(path_to_file, "r")
    for line in f:
        if line == "\n" or line == "\r" or line == "\r\n":
            if len(holder) > 0:
                retval.append(holder)
                holder = []
        else:
            x = line.strip()
            piece = X(x)
            holder.append(piece)
    if len(holder) > 0:
        retval.append(holder)
    return retval


if __name__ == "__main__":
    filepath = sys.argv[2]
    if sys.argv[1] == "xy":
        d = parse_xy(filepath)
    elif sys.argv[1] == "x":
        d = parse_x(filepath)
    else:
        raise Exception("Invalid mode.")
    for i in d:
        for p in i:
            print p
        print ""
