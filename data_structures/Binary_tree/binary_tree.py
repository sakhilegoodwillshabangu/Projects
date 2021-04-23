class BinaryTree:
	def __init__(self):
		self.tree = EmptyNode()
	def search(self, value):
		return self.tree.inOderSearch(value)
	def insert(self, value):
		return self.tree.insert(value)
class EmptyNode:
	def search(self, value):
		return False
	def insert(self, value):
		return BinaryNode(self, value, self)
class BinaryNode:
	def __init__(self, left, value, right):
		self.left, self.right, self.value = left, value, right
	def inOderSearch(self, value):
		if self.value == value:
			return True
		elif self.value > value:
			return self.right.inOrderSearch(value)
		elif self.value < value:
			return self.left.inOderSearch(value)
	def preOderSearch(self, value):
		if self.value == value:
			return True
		self.right.preOderSearch(value)
		self.left.preOderSearch(value)
	def postOderSearch(self, value):
		self.right.postOderSearch(value)
		self.left.postOderSearcb(value)
		if self.value == value:
			return True
	def insert(self, value):
		if self.value > value:
			self.right = self.right.insert(value)
		elif self.value < value:
			self.left = self.left.insert(value)
		return self