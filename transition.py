from classes import *
import parse as ps
import sys
import filewriter
from emission import *
import comparator


# An object that computes and contains the transition parameters.
class TransitionParameters:
	def __init__(self):
		self.transitions = {}
		self.states = {}

	# Train the parameters with a node.
	#
	# Params:
	# tag - A Tag object
	def train(self, tag):
		if isinstance(tag, Stop):
			return
		k = (tag.name, tag.next_tag.name)
		try:
			self.transitions[k] += 1
		except KeyError:
			self.transitions[k] = 1
		try:
			self.states[tag.name] += 1
		except KeyError:
			self.states[tag.name] = 1

	# Get the transition parameters for a given tag name and word value.
	#
	# Params:
	# tag1 - The name of y(i) Tag
	# tag2 - The name of y(i+1) Tag
	def get(self, tag1, tag2):
		k = (tag1, tag2)
		try:
			return float(self.transitions[k])/float(self.states[tag1])
		except KeyError:
			return 0.0


# Train the transition parameters using the training data.
#
# Params:
# seqs - A list of lists of StateNode objects, such as those obtained from parser.parse_xy()
#
# Returns:
# A trained EmissionParameters object.
def train_transition(seqs):
	tracker = TransitionParameters()
	for seq in seqs:
		for node in seq:
			tracker.train(node)
	return tracker
