#!~/anaconda/bin/python
#


from classes import *
import parser


class EmissionParameters:
    def __init__(self):
        self.emissions = {}
        self.states = {}

    def train(self, y):
        if isinstance(y, SpecialNode):
            return
        key = (y.label, y.x.value)
        try:
            self.emissions[key] += 1
        except KeyError:
            self.emissions[key] = 1
        try:
            self.states[y.label] += 1
        except KeyError:
            self.states[y.label] = 1

    def get(self, y, x):
        if isinstance(y, SpecialNode):
            return 0
        key = (y, x)
        try:
            return float(self.emissions[key])/float(self.states[y])
        except KeyError:
            return 1.0/float(self.states[y] + 1)

def train_emission(path_to_file):
    pass

if __name__ == "__main__":
    pass
