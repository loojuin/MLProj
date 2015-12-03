from transition import *
from emission import *
from classes import *

import parse
import filewriter
import comparator


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
	class ViterbiNode:
		def __init__(self, word, tag_name, prev_node_list):
			self.word = word
			self.tag_name = tag_name
			self.p = -1.0
			self.parent = None
			if len(prev_node_list) == 0:
				self.p = trans_params.get("", self.tag_name) * emiss_params.get(self.tag_name, self.word.value)
			for node in prev_node_list:
				cur_p = node.p * trans_params.get(node.tag_name, self.tag_name) * emiss_params.get(self.tag_name, self.word.value)
				if cur_p > self.p:
					self.p = cur_p
					self.parent = node

	retval = []

	for word_seq in word_seqs:
		node_layers = [[]]
		for word in word_seq:
			layer = []
			for tag in tag_names:
				layer.append(ViterbiNode(word, tag, node_layers[-1]))
			node_layers.append(layer)

		last_layer = node_layers[-1]
		last_node = None
		p = -1
		for node in last_layer:
			cur_p = trans_params.get(node.tag_name, "")
			if cur_p > p:
				last_node = node
				p = cur_p

		cur_tag = Stop()
		cur_node = last_node
		while cur_node is not None:
			new_tag = Tag(cur_node.tag_name, cur_node.word, cur_tag)
			cur_tag = new_tag
			cur_node = cur_node.parent
		start = Start(cur_tag)
		retval.append(start.to_list())

	return retval


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Not enough arguments. Usage: $ python viterbi.py [training file] [testing file] [output file]"
		quit(0)
	train = sys.argv[1]
	test = sys.argv[2]
	output = sys.argv[3]
	xy_train, tags = parse.parse_xy(train)
	x_test = parse.parse_x(test)
	xy_test, junk = parse.parse_xy(test)
	emiss_params = train_emission(xy_train)
	trans_params = train_transition(xy_train)
	xy_pred = viterbi_predict(x_test, emiss_params,	trans_params, tags)
	filewriter.write_file(xy_pred, output)
	acc = comparator.calculate_accuracy(xy_pred, xy_test)
	for seq in xy_pred:
		for node in seq:
			print node
		print ""
	print "Accuracy: %f" % acc
