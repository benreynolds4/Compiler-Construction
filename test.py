# Ben Reynolds 13309656
# Task2  (Test) - Assignment 1
from LexicalAnalyzier import *
from Trie import *

Lexer = Lexer()
Lexer.driver()
#Lexer.printTrie()


trie = Trie()
trie.proccessWord("private")
trie.proccessWord("public")
trie.proccessWord("protected")
trie.proccessWord("static")
trie.proccessWord("primary")
trie.proccessWord("integer")
trie.proccessWord("exception")
trie.proccessWord("try")
