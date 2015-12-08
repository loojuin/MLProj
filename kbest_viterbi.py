#!~/anaconda/bin/python
#
# This module contains the logic for performing kth-best predictions with a modified Viterbi algorithm.
#
# Running this module from the command line would perform a complete training and prediction cycle,
# with the final tagged sequence being printed to a file, and also reporting the accuracy of the predictions.


from transition import *
from emission import *
from classes import *
from helpers import *

import parse
import filewriter
import comparator
import time


# Predict the k-th best tags for a given sequence of Word objects using a modified Viterbi Algorithm.
#
# Params:
# word_seqs - A list of lists of Word objects, such as those obtained from parser.parse_x()
# emiss_params - The trained EmissionParameters object
# trans_params - The trained TransitionParameters object
# tag_names - A list of the possible tag names, such as would be obtained from parser.parse_xy()
# k - Parameter for the desired ranking
#
# Returns:
# A list of lists of StateNode objects.
def kbest_viterbi_predict(word_seqs, emiss_params, trans_params, tag_names, k):

	# A class representing a Tag candidate, and also an entry in the "Pi" table.
	#
	# It is similar to the Tag class, except that instead of being forward-linked, it is
	# backward-linked (i.e., instead of containing a reference to the next node, it contains
	# a reference to the previous node).
	#
	# It also contains the probability value.
	class KBestViterbiNode:
		# Create a new KBestViterbiNode object.
		#
		# Performs the maximum likelihood estimation when instantiated.
		#
		# Params:
		# word - The Word object that is associated with this Tag candidate.
		# tag_name - The name of the tag that this node represents.
		# prev_node_list - A list of all node candidates associated with the previous word in the sequence.
		def __init__(self, word, tag_name, p, parent):
			self.word = word
			self.tag_name = tag_name
			self.p = p
			self.parent = parent

	# Get the best k lineages for a particular word and tag.
	#
	# Params:
	# word - The Word object to be associated with this tag.
	# tag_name - The name of the tag.
	# prev_layer - A list of nodes associated with the previous word in the sequence.
	#
	# Returns:
	# A list of KBestViterbiNode objects with the same tag and associated with the same word.
	def get_k_best_parents(word, tag_name, prev_layer):
		if len(prev_layer) == 0:
			e = emiss_params.get(tag_name, word.value)
			t = trans_params.get("", tag_name)
			return [KBestViterbiNode(word, tag_name, e*t, None)]
		buffer = BestFirstBoundedSortedList(k, lambda n: n.p)
		for node in prev_layer:
			e = emiss_params.get(tag_name, word.value)
			t = trans_params.get(node.tag_name, tag_name)
			l = node.p*e*t
			buffer.put(KBestViterbiNode(word, tag_name, l, node))
		# buffer.integrity_check()  # For debugging.
		return buffer.list

	retval = []

	likelihoods = 0.0

	for word_seq in word_seqs:
		current_layer = []
		for word in word_seq:
			upcoming_layer = []
			for tag in tag_names:
				upcoming_layer.extend(get_k_best_parents(word, tag, current_layer))
			current_layer = upcoming_layer

		final_buffer = BestFirstBoundedSortedList(k, lambda n: n.p)
		for node in current_layer:
			t = trans_params.get(node.tag_name, "")
			l = node.p * t
			final_buffer.put(KBestViterbiNode(None, "", l, node))
		last_node = final_buffer.list[-1].parent

		likelihoods += final_buffer.list[-1].p

		cur_tag = Stop()
		cur_node = last_node
		while cur_node is not None:
			new_tag = Tag(cur_node.tag_name, cur_node.word, cur_tag)
			cur_tag = new_tag
			cur_node = cur_node.parent
		start = Start(cur_tag)
		retval.append(start.to_list())

	print "%d-th best likelihood:" % k, likelihoods/len(retval)

	return retval


if __name__ == "__main__":
	if len(sys.argv) != 5:
		print "Not enough arguments. Usage: $ python kbest_viterbi.py [k] [training file] [testing file] [output file]"
		quit(0)
	k = int(sys.argv[1])
	train = sys.argv[2]
	test = sys.argv[3]
	output = sys.argv[4]
	parse_start = time.time()
	xy_train, tags = parse.parse_xy(train)
	x_test = parse.parse_x(test)
	xy_test, junk = parse.parse_xy(test)
	parse_end = time.time()
	print "Finished parsing."
	train_start = time.time()
	emiss_params = train_emission(xy_train)
	trans_params = train_transition(xy_train)
	train_end = time.time()
	print "Finished training."
	pred_start = time.time()
	xy_pred = kbest_viterbi_predict(x_test, emiss_params, trans_params, tags, k)
	pred_end = time.time()
	filewriter.write_file(xy_pred, output)
	acc = comparator.calculate_accuracy(xy_pred, xy_test)
	# for seq in xy_pred:
	# 	for node in seq:
	# 		print node
	# 	print ""
	print "Time taken to parse: %f s" % (parse_end - parse_start)
	print "Time taken to train: %f s" % (train_end - train_start)
	print "Time taken to predict: %f s" % (pred_end - pred_start)
	print "Accuracy: %f" % acc
