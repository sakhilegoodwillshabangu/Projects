class LinkedList:
	def __init__(self):
		self.list = EmptyNode()
		self.counter = 0
	def __repr__(self):
		return repr(self.list)
	def lookup(self, item):
		self.list.lookup(item)
	def insert(self, item):
		self.list = self.list.insert(item)
	def getLength(self):
		counter = self.list.getLength()
		return counter
	def getItem(self, index):
		return self.list.getItem(index)
	def changeItem(self, item, index):
		return self.list.changeItem(item, index)
	def index(self, item):
		return self.list.index(item)
	def reverseItems(self):
		if self.counter != (self.getLength()//2):
			item_one = self.getItem(self.counter)
			self.counter+= 1
			item_two = self.getItem(self.getLength() - self.counter)
			self.changeItem(item_two, self.counter - 1)
			self.changeItem(item_one, self.getLength() - self.counter)
			self.reverseItems()
		return self
	def deleteItem(self, item):
		self.list.deleteItem(item)
	def pop(self, index):
		self.list.pop(index)
	def sort(self):
		self.list.sort()
class EmptyNode:
	def __repr__(self):
		return "*"
	def lookup(self, item):
		print("False")
		return False
	def insert(self, item):
		return ListNode(self, item)
	def getLength(self):
		return 0
	def getItem(self, index):
		pass
	def changeItem(self, item, index):
		raise IndexError("index outside list bounds")
	def deleteItem(self, item):
		raise ValueError(str(item) + " does not exist")
	def reverseItems(self):
		return None
	def index(self, item):
		raise ValueError(str(item) + " does not exist")
	def pop(self, index):
		raise IndexError("index: " + str(index) + " is outside list bounds")
	def sort(self):
		pass
class ListNode:
	def __init__(self, node, item):
		self.counter = 0
		self.size = 0
		self.parent = self
		self.node, self.item = node, item
	def __repr__(self):
		return "item is = %s" % repr(self.item)
	def lookup(self, item):
		if self.item == item:
			print(True)
			return True
		else:
			return self.node.lookup(item)
	def insert(self, item):
		self.node.parent = self
		self.node = self.node.insert(item)
		return self
	def getLength(self):
		return self.node.getLength() + 1
	def getItem(self, index):
		if (index == 0):
			return self.item
		else:
			item = self.node.getItem(index - 1)
		return item
	def changeItem(self, item, index):
		if (index == 0):
			self.item = item
		else:
			self.node.changeItem(item, index - 1)
	def index(self, item):
		if self.item == item:
			return 0
		return self.node.index(item) + 1
	def deleteItem(self, item):
		if self.item == item:
			if self == self.parent:
				next_node = self.node
				self.item = self.node.item
				self.parent.node = next_node.node
			else:
				next_node = self.node
				self.parent.node = next_node
		else:
			self.node.deleteItem(item)
	def pop(self, index):
		item = self.getItem(index)
		self.deleteItem(item)	

	