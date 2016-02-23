from Trie import Trie

class DFA:
    def __init__(self):                      # initialise the DFA class with the 5 elements in DFA
        self.file = open("input9.txt")
        self.Trie = Trie()
        self.putback_bool, self.putback_val = False, ""
        self.current_state, self.current_word = 0, ""
        self.states = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}        # 8 is putback and 9 is error
        uppercase, lowercase = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                                 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                 'Y', 'Z'} , { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                                 'w', 'x', 'y', 'z'}
        whitespace, numbers = {'\t', '\n', ' '} , { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' }

        delta = dict()                        # Set up the delta function for each state.
        for letter in uppercase:
            delta[(0, letter)] = 1
            delta[(4, letter)] = 4
            delta[(6, letter)] = 4
            # Move to error state i.e. State 8
            delta[(1, letter)] = 9      # e.g. aaB  error
            delta[(2, letter)] = 9      # e.g. AaB  error
            delta[(3, letter)] = 8      # e.g. 0B   check
            delta[(7, letter)] = 9      # e.g. ;B   check
            
        for letter in lowercase:
            delta[(0, letter)] = 2      
            delta[(1, letter)] = 1
            delta[(2, letter)] = 2
            delta[(4, letter)] = 4
            delta[(6, letter)] = 4
            # Move to error state i.e. State 8
            delta[(3, letter)] = 8      # e.g. 0a  check
            delta[(7, letter)] = 9      # e.g. ;b  error
            
        for number in numbers:
            delta[(0, number)] = 3
            delta[(3, number)] = 3
            delta[(6, number)] = 4
            # Move to error state i.e. State 8
            delta[(1, number)] = 8      # e.g. a1 check a
            delta[(2, number)] = 8      # e.g. As1 check As
            delta[(7, number)] = 9      # e.g. ;0 error
        
        for space in whitespace:
            delta[(0, space)] = 0
            delta[(4, space)] = 4
            delta[(6, space)] = 4

        delta[(0, '"')] = 4
        delta[(0, ')')] = 7
        delta[(0, '(')] = 7
        delta[(0, ';')] = 7
        delta[(4, '"')] = 5
        delta[(4, '~')] = 6
        delta[(6, '~')] = 4
        delta[(6, '"')] = 4

        self.delta = delta
        self.starting_state = {0}
        self.accepting_states = {1,2,3,5,7}
    
    def transition_state(self, input):
                 # if the transition is not defined then set current_state starte as None
        if ((self.current_state, input) not in self.delta.keys()):         
            return False
        else:                                       # else change the current_state state
            self.current_state = self.delta[(self.current_state, input)]            
            
    def run_char(self, input):
        print str(self.current_state) + ' ' + input + ' ' + self.current_word
        if (input == '\t' or input == '\n' or input == ' ') and  self.current_state != 4:
            boolean = self.in_accepting_state()
            identifier = self.checkIdentifier(boolean)
            if identifier != "ERROR":
                self.Trie.proccessWord(self.current_word)
            self.resetTrackedVariables()
            return identifier
        else:
            if not self.putback_bool:                   # if putback is false
                self.transition_state(input)            
                if self.current_state != 8:
                    if input != "~":
                        self.current_word = self.current_word + input
                    return "WORD NOT COMPLETE"
                else:
                    self.set_putback(input)
                    self.Trie.proccessWord(self.current_word)
                    self.resetTrackedVariables()
                    return "CANT GET ID YET"
            elif self.putback_bool:
                self.transition_state(self.putback())
                if self.current_state != 8:
                    if input != "~" or input != '"':
                        self.current_word = self.current_word + input

            return "Not End"

    def printTrie(self):
        self.Trie.printTrie()

    def resetTrackedVariables(self):
        self.current_state = 0
        self.current_word = ""

    def putback(self):
        self.putback_bool = False
        return self.putback_val

    def set_putback(self, character):
        self.putback_bool = True
        self.putback_val = character

    def checkIdentifier(self, boolean):
        if boolean:                                   #check if in accepting state 
            if self.current_state == 1 or self.current_state == 2:
                return "ID"    
            elif self.current_state == 3:
                return "INT" 
            elif self.current_state == 5:
                return "STRING"
            elif self.current_state == 7:
                if self.current_word == '(':
                    return 'LPAR'
                elif self.current_word == ')':
                    return 'RPAR'
                elif self.current_word == ';':
                    return 'SEMICOLON'
        else:
            return "ERROR"

    def driver(self):
        with self.file as f:
            while True:
                if self.putback_bool:
                    self.run_char(self.putback())
                else:
                    c = f.read(1)
                    if not c:
                        print "End of file"
                        break
                    print self.run_char(c)  
        self.printTrie()

    def in_accepting_state(self):                                       
        return self.current_state in self.accepting_states

            
        

    



        





