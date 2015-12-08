#!~/anaconda/bin/python
#

class BestFirstBoundedSortedList:
		def __init__(self, k, comp_func):
			self.bound = k
			self.list = []
			self.comp = comp_func

		def put(self, obj):
			if len(self.list) == 0:
				self.list.append(obj)
				return
			inserted = False
			for i in range(len(self.list)):
				if self.comp(self.list[i]) < self.comp(obj):
					self.list.insert(i, obj)
					inserted = True
					if len(self.list) > self.bound:
						self.list.pop()
					break
			if (not inserted) and (len(self.list) < self.bound):
				self.list.append(obj)

		def integrity_check(self):
			if len(self.list) > self.bound:
				raise Exception("Error! BestFirstBoundedSortedList length exceeded the bound.")
			for i in range(len(self.list) - 1):
				if self.comp(self.list[i]) < self.comp(self.list[i + 1]):
					raise Exception("Error! BestFirstBoundedSortedList has misordered elements.")