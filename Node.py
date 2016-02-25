# Ben Reynolds 13309656
# Task1 - Assignment 1
# Node Class allows you to create each node for the Trie.
class Node:
	def __init__(self, character, ID):
		self.character = character
		self.ID = ID
		self.nextNodes = []
		self.accepting = False

	def getCharacter(self):
		return self.character

	def setAccepting(self):
		self.accepting = True

	def addNextNode(self, node):
		self.nextNodes.append(node)

	def getConnectedNodes(self):
		return self.nextNodes