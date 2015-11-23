#!~/anaconda/bin/python
#


import sys

class Node:
    def __init__(self):
        pass


class Start(Node):
    def __init__(self, next_y):
        self.next_y = next_y

    def __str__(self):
        return "START"

    def __repr__(self):
        return str(self)

    def to_list(self):
        retval = [self]
        return self.next_y.to_list(retval)


class Stop(Node):
    def __init__(self):
        pass

    def __str__(self):
        return "STOP"

    def __repr__(self):
        return str(self)

    def to_list(self, ls):
        ls.append(self)
        return ls


class Y(Node):
    def __init__(self, label, x, next_y = Stop()):
        self.label = label
        self.x = x
        self.next_y = next_y

    def __str__(self):
        return "%s => %s" % (self.label, self.x)

    def __repr__(self):
        return str(self)

    def to_list(self, ls):
        ls.append(self)
        return self.next_y.to_list(ls)


class X(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)


def parse_xy(path_to_file):
    retval = []
    stop = Stop()
    start = Start(stop)
    pointer = start
    f = open(path_to_file, "r")
    for line in f:
        if line == "\n" or line == "\r" or line == "\r\n":
            if pointer != start:
                retval.append(start.to_list())
                stop = Stop()
                start = Start(stop)
                pointer = start
        else:
            linesplit = line.strip().split(" ")
            x = linesplit[0]
            y = linesplit[1]
            new_x = X(x)
            new_y = Y(y, new_x, stop)
            pointer.next_y = new_y
            pointer = new_y
    if pointer != start:
        retval.append(start.to_list())
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
            linesplit = line.strip().split(" ")
            x = linesplit[0]
            new_x = X(x)
            holder.append(new_x)
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
        print "Invalid mode."
        quit(0)
    for i in d:
        for p in i:
            print p
        print ""
