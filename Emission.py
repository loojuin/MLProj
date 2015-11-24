#!~/anaconda/bin/python
#


from classes import *
import parser
import sys
import filewriter


class EmissionParameters:
    def __init__(self):
        self.emissions = {}
        self.states = {}

    def train(self, y):
        if isinstance(y, SpecialNode):
            return
        k = (y.label, y.x.value)
        try:
            self.emissions[k] += 1
        except KeyError:
            self.emissions[k] = 1
        try:
            self.states[y.label] += 1
        except KeyError:
            self.states[y.label] = 1

    def get(self, ylabel, xvalue):
        k = (ylabel, xvalue)
        try:
            return float(self.emissions[k])/float(self.states[ylabel])
        except KeyError:
            return 1.0/float(self.states[ylabel] + 1)


def train_emission(seqs):
    tracker = EmissionParameters()
    for seq in seqs:
        for node in seq:
            tracker.train(node)
    return tracker


def emission_predict(xseqs, params, labels):
    def argmax_y(xvalue):
        currentL = None
        currentP = 0.0
        for l in labels:
            p = params.get(l, xvalue)
            if p > currentP:
                currentL = l
                currentP = p
        return currentL

    xyseqs = []
    for seq in xseqs:
        stop = Stop()
        start = Start(stop)
        current = start
        for node in seq:
            ylabel = argmax_y(node.value)
            newnode = Y(ylabel, node, stop)
            current.next_y = newnode
            current = newnode
        xyseqs.append(start.to_list())
    return xyseqs


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Not enough arguments. Usage: $ python emission.py [training file] [testing file] [output file]"
        quit(0)
    train = sys.argv[1]
    test = sys.argv[2]
    output = sys.argv[3]
    xy_train = parser.XYParse(train)
    x_test = parser.XParse(test)
    params = train_emission(xy_train.seqs)
    xy_pred = emission_predict(x_test.seqs, params, xy_train.tags)
    filewriter.write_file(xy_pred, output)
    for seq in xy_pred:
        for node in seq:
            print node
        print ""

