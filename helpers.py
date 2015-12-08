#!~/anaconda/bin/python
#
# This module contains helper classes and methods.


# This class is basically a bounded buffer that enforces the following invariants:
# - The first element in the buffer always has the highest value (according to some
#   value function).
# - The elements in the buffer are always sorted in descending order according to
#   the value function.
# - The elements in the buffer are always the top k of all elements that have ever
#   been put in the buffer since the buffer's instantiation.
class BestFirstBoundedSortedList:
	# Params:
	# k - The size of the buffer
	# val_func - The value function to be used on the elements
	def __init__(self, k, val_func):
		self.bound = k
		self.list = []
		self.val = val_func

	# Attempt to put an object in the buffer.
	#
	# The object will only be inserted if its value is within the
	# top k of all elements ever inserted into the buffer.
	#
	# Params:
	# obj - The object
	def put(self, obj):
		if len(self.list) == 0:
			self.list.append(obj)
			return
		inserted = False
		for i in range(len(self.list)):
			if self.val(self.list[i]) < self.val(obj):
				self.list.insert(i, obj)
				inserted = True
				if len(self.list) > self.bound:
					self.list.pop()
				break
		if (not inserted) and (len(self.list) < self.bound):
			self.list.append(obj)

	# Check that the invariants are held.
	def integrity_check(self):
		if len(self.list) > self.bound:
			raise Exception("Error! BestFirstBoundedSortedList length exceeded the bound.")
		for i in range(len(self.list) - 1):
			if self.val(self.list[i]) < self.val(self.list[i + 1]):
				raise Exception("Error! BestFirstBoundedSortedList has misordered elements.")