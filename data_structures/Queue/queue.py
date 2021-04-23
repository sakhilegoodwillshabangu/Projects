class Queue:
	def __init__(self):
		self.linked_list = LinkedList()
	def push(self, item):
		self.linked_list.insert(item)
	def pop(self):
		top_item = self.linked_list.pop(0)
		return top_item
	def top(self):
		return self.linked_list.getItem(0)
	def length(self):
		return self.linked_list.getLength()