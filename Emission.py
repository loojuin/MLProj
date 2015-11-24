#!~/anaconda/bin/python
#


from classes import *
import parser
import sys


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

    def get(self, y):
        if isinstance(y, SpecialNode):
            return 0
        k = (y.label, y.x.value)
        try:
            return float(self.emissions[k])/float(self.states[y.label])
        except KeyError:
            return 1.0/float(self.states[y.label] + 1)


def train_emission(seqs):
    tracker = EmissionParameters()
    for seq in seqs:
        for node in seq:
            tracker.train(node)
    return tracker


if __name__ == "__main__":
    file_to_parse = sys.argv[1]
    parse = parser.XYParse(file_to_parse)
    seqs = parse.seqs
    params = train_emission(seqs)
    for seq in seqs:
        for node in seq:
            if isinstance(node, SpecialNode):
                continue
            print node, params.get(node)

