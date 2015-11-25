#!~/anaconda/bin/python
#
# This module contains the logic for computing the emission parameters for a tag-word sequence.
#
# Running this module from the command line would perform a complete training and prediction cycle,
# with the final tagged sequence being printed to the console, and also the accuracy of the predictions.


from classes import *
import parser
import sys
import filewriter
import comparator


# An object that computes and contains the emission parameters.
class EmissionParameters:
    def __init__(self):
        self.emissions = {}
        self.states = {}

    # Train the parameters with one node.
    #
    # Params:
    # tag - A Tag object
    def train(self, tag):
        if isinstance(tag, SpecialNode):
            return
        k = (tag.name, tag.word.value)
        try:
            self.emissions[k] += 1
        except KeyError:
            self.emissions[k] = 1
        try:
            self.states[tag.name] += 1
        except KeyError:
            self.states[tag.name] = 1

    # Get the emission parameters for a given tag name and word value.
    #
    # Params:
    # tag_name - The name of a tag
    # word_value - The literal word
    def get(self, tag_name, word_value):
        k = (tag_name, word_value)
        try:
            return float(self.emissions[k])/float(self.states[tag_name] + 1)
        except KeyError:
            return 1.0/float(self.states[tag_name] + 1)


# Train the emission parameters using the training data.
#
# Params:
# seqs - A list of lists of StateNode objects, such as those obtained from parser.parse_xy()
#
# Returns:
# A trained EmissionParameters object.
def train_emission(seqs):
    tracker = EmissionParameters()
    for seq in seqs:
        for node in seq:
            tracker.train(node)
    return tracker


# Predict the tags for a given sequence of Word objects.
#
# Params:
# word_seqs - A list of lists of Word objects, such as those obtained from parser.parse_x()
# params - The trained EmissionParameters object
# tag_names - A list of the possible tag names, such as would be obtained from parser.parse_xy()
#
# Returns:
# A list of lists of StateNode objects.
def emission_predict(word_seqs, params, tag_names):
    def argmax_y(xvalue):
        currentL = None
        currentP = 0.0
        for l in tag_names:
            p = params.get(l, xvalue)
            if p > currentP:
                currentL = l
                currentP = p
        return currentL

    xyseqs = []
    for seq in word_seqs:
        stop = Stop()
        start = Start(stop)
        current = start
        for node in seq:
            ylabel = argmax_y(node.value)
            newnode = Tag(ylabel, node, stop)
            current.next_tag = newnode
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
    xy_train, tags = parser.parse_xy(train)
    x_test = parser.parse_x(test)
    xy_test, junk = parser.parse_xy(test)
    params = train_emission(xy_train)
    xy_pred = emission_predict(x_test, params, tags)
    filewriter.write_file(xy_pred, output)
    acc = comparator.calculate_accuracy(xy_pred, xy_test)
    for seq in xy_pred:
        for node in seq:
            print node
        print ""
    print "Accuracy: %f" % acc
