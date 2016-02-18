import re
from Task1 import Trie
class DFA:
    def __init__(self):                                                 # initialise the DFA class with the 5 elements in DFA
        self.states = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 }
        uppercase = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                      'Y', 'Z'}
        lowercase = { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                      'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                      'w', 'x', 'y', 'z'}
        whitespace = {'\t', '\n', ' '}
        numbers = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' }

        delta = dict()                                                  # Set up the delta function for each state.
        for letter in uppercase:
            delta[(0, letter)] = 1
            delta[(4, letter)] = 4
            
        for letter in lowercase:
            delta[(0, letter)] = 2
            delta[(1, letter)] = 1
            delta[(2, letter)] = 2
            delta[(4, letter)] = 4
            
        for number in numbers:
            delta[(0, number)] = 3
            delta[(3, number)] = 3
        
        for space in whitespace:
            delta[(1, space)] = 10
            delta[(2, space)] = 11
            delta[(3, space)] = 12

        delta[(0, '"')] = 4
        delta[(0, ')')] = 7
        delta[(0, '(')] = 8
        delta[(0, ';')] = 9
        delta[(4, '"')] = 5
        delta[(4, '~')] = 6
        delta[(6, '~')] = 4
        delta[(6, '"')] = 4

        self.delta = delta
        print delta
        self.starting_state = {0}
        self.accepting_states = {5, 7, 8, 9, 10, 11, 12}
    
    def transition_state(self, input):
        if ((self.current, input) not in self.delta.keys()):          # if the transition is not defined then set current starte as None
            #print "Incorrect input or transition" + str(self.current)  + input
            return False
        else:
            self.current = self.delta[(self.current, input)]            # else change the current state
            if self.current == 10 or self.current == 11 or self.current == 12:
                #Add to symbol trie 
                self.current = 0
        
    def in_accepting_state(self):                                       
        return self.current in self.accepting_states
    
    def play(self, input):
        self.current = 0;                                               # set first state as the current one
        for character in input:                                         #loop threw input transitioning
            self.transition_state(character)
            
        if self.in_accepting_state():                                   #check if in accepting state     
            #Add to the symbol table etc.     
            return True
        else:
            return False


d = DFA()
Trie = Trie()

txt = open("test-input.txt")
for line in txt:
    split_words = line.split()
    for words in split_words:
        words = words + " "
        if d.play(line):
            print words
            print "String is accepting"
            Trie.proccessWord(words)
        else:
            print words
            print "String is not accepting"


