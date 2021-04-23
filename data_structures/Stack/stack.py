from linked_list import *
class Stack:
	def __init__(self):
		self.linked_list = LinkedList()
	def push(self, item):
		self.linked_list.insert(item)
	def pop(self):
		length = self.linked_list.getLength()
		top_item = self.linked_list.pop(length - 1)
		return top_item
	def top(self):
		length = self.linked_list.getLength()
		top_item = self.linked_list.getItem(length - 1)
		return top_item
	def length(self):
		return self.linked_list.getLength()