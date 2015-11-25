#!~/anaconda/bin/python
#
# This module contains the logic for comparing StateNode sequences,
# and reporting the accuracy of prediction algorithms.


#
def calculate_accuracy(pred_seqs, test_seqs):
    if len(pred_seqs) != len(test_seqs):
        raise Exception("The list of node sequences do not match.")
    total = 0
    correct = 0
    for i in range(len(pred_seqs)):
        pred_seq = pred_seqs[i]
        test_seq = test_seqs[i]
        if len(pred_seq) != len(test_seq):
            raise Exception("Found a node sequence that does not match.")
        for j in range(1, len(pred_seq) - 1, 1):
            pred = pred_seq[j]
            test = test_seq[j]
            if pred.word.value != test.word.value:
                raise Exception("Found a node that has non-matching x value.")
            if pred.name == test.name:
                correct += 1
            total += 1
    return float(correct)/float(total)