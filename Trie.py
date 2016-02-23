class Trie:
	def __init__(self):
		self.Nodes = []
		self.root = Node("", 0)
		self.Nodes.append(self.root)
		self.currentNode = self.root

	def checkLetter (self, flag, character):
		# Take a flag and a character, If flag is true trie is dynamic, else its static. 
		# If character exists return true else return false unless it's dynamic in which case add it.
		# True for Dynamic  - False for Static
		
		if flag == True:
			connectedNodes = self.currentNode.getConnectedNodes()
			for node in connectedNodes:
				if node.getCharacter() == character:
					self.currentNode = node 
					return True

			newNode = Node(character, self.pickNewID())
			self.currentNode.addNextNode(newNode)
			self.Nodes.append(newNode)
			self.currentNode = newNode
			return True
		else:
			connectedNodes = self.currentNode.getConnectedNodes()
			for node in connectedNodes:
				if node.getCharacter() == character:
					self.currentNode = node 
					return True
			return False


	def checkWordExists(self, word):
		# check if word in tree if it is return ID, id dynamic and there but not accepting make accepting and return
		# that ID else return negative id. 
		self.setRoot()
		dynamincFlag = True
		if word[:1].isupper():		#Check first letter in word.
			dynamincFlag = False

		lettersExist = True
		for character in word:
			connectedNodes = self.currentNode.getConnectedNodes()
			for node in connectedNodes:
				if node.character == character:
					self.currentNode = node
					lettersExist = True
					break
				else:
					lettersExist = False
					

		if lettersExist and not dynamincFlag:
			self.currentNode.setAccepting()
			return self.currentNode.ID
		elif lettersExist and self.currentNode.accepting == True:
			return self.currentNode.ID

	def proccessWord(self, word):
		#Method takes a word and tries to add said word using method one, and two to check its ID. 
		self.setRoot()
		dynamincFlag = True
		if word[:1].isupper():		#Check first letter in word.
			dynamincFlag = False

		for w in word:
			self.checkLetter(dynamincFlag, w)

		if dynamincFlag:
			self.currentNode.setAccepting()

		#print self.checkWordExists(word)

	def setRoot(self):
		self.currentNode = self.root

	def pickNewID(self): 
		currentHighest = 0
		for node in self.Nodes:
			if node.ID > currentHighest:
				currentHighest = node.ID
		return currentHighest + 1

	def printTrie(self):
		for node in self.Nodes:
			print str(node.ID) + " " + node.character + " " + str(node.accepting)
			for nextNode in node.nextNodes:
				print nextNode.getCharacter()
			print "\n"


# Node Class allows you to create each node for the Trie. 
# A Node stores an ID, A character, an array of Nodes it's connected to and also whether the node is accepting or not.
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


#TESTING 

trie = Trie()
trie.proccessWord("private")
trie.proccessWord("public")
trie.proccessWord("protected")
trie.proccessWord("static")
trie.proccessWord("primary")
trie.proccessWord("integer")
trie.proccessWord("exception")
trie.proccessWord("try")



