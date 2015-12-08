from transition import *
from emission import *
from classes import *

import parse
import filewriter
import comparator
import time


# Predict the tags for a given sequence of Word objects using the Viterbi Algorithm.
#
# Params:
# word_seqs - A list of lists of Word objects, such as those obtained from parser.parse_x()
# emiss_params - The trained EmissionParameters object
# trans_params - The trained TransitionParameters object
# tag_names - A list of the possible tag names, such as would be obtained from parser.parse_xy()
#
# Returns:
# A list of lists of StateNode objects.
def viterbi_predict(word_seqs, emiss_params, trans_params, tag_names):
	# A class representing a Tag candidate, and also an entry in the "Pi" table.
	#
	# It is similar to the Tag class, except that instead of being forward-linked, it is
	# backward-linked (i.e., instead of containing a reference to the next node, it contains
	# a reference to the previous node).
	#
	# It also contains the probability value.
	class ViterbiNode:
		# Create a new ViterbiNode object.
		#
		# Performs the maximum likelihood estimation when instantiated.
		#
		# Params:
		# word - The Word object that is associated with this Tag candidate.
		# tag_name - The name of the tag that this node represents.
		# prev_node_list - A list of all node candidates associated with the previous word in the sequence.
		def __init__(self, word, tag_name, prev_node_list):
			self.word = word
			self.tag_name = tag_name
			self.p = -1.0
			self.parent = None
			if len(prev_node_list) == 0:
				self.p = trans_params.get("", self.tag_name) * emiss_params.get(self.tag_name, self.word.value)
				return
			for node in prev_node_list:
				cur_p = node.p * trans_params.get(node.tag_name, self.tag_name) * emiss_params.get(self.tag_name, self.word.value)
				if cur_p > self.p:
					self.p = cur_p
					self.parent = node

	retval = []
	likelihoods = 0.0

	for word_seq in word_seqs:
		current_layer = []
		for word in word_seq:
			upcoming_layer = []
			for tag in tag_names:
				upcoming_layer.append(ViterbiNode(word, tag, current_layer))
			current_layer = upcoming_layer

		last_layer = current_layer
		last_node = None
		p = -1.0
		for node in last_layer:
			cur_p = node.p * trans_params.get(node.tag_name, "")
			if cur_p > p:
				last_node = node
				p = cur_p

		likelihoods += p

		cur_tag = Stop()
		cur_node = last_node
		while cur_node is not None:
			new_tag = Tag(cur_node.tag_name, cur_node.word, cur_tag)
			cur_tag = new_tag
			cur_node = cur_node.parent
		start = Start(cur_tag)
		retval.append(start.to_list())

	print "Average maximum likelihood:", likelihoods / len(retval)

	return retval


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Not enough arguments. Usage: $ python viterbi.py [training file] [testing file] [output file]"
		quit(0)
	train = sys.argv[1]
	test = sys.argv[2]
	output = sys.argv[3]
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
	xy_pred = viterbi_predict(x_test, emiss_params,	trans_params, tags)
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
