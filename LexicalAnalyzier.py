# Ben Reynolds 13309656
# Task2 - Assignment 1

from Trie import Trie

class Lexer:
    def __init__(self):                      # initialise the DFA class with the 5 elements in DFA
        self.file = open("input3.txt")
        self.Trie = Trie()
        self.putback_bool, self.putback_val = False, ""
        self.current_state, self.current_word = 0, ""
        self.previous_word = ""
        self.previous_state = 0
        self.states = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}        # 8 is putback and 9 is error
        self.starting_state = {0}
        self.accepting_states = {1,2,3,5,7}
        uppercase, lowercase = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                    'Y', 'Z'} , { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',  'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                    'w', 'x', 'y', 'z'}
        whitespace, numbers = {'\t', '\n', ' '},  { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' }
        invalids = {'?', '-', '_', '+', '|', ',', '.'}

        delta = dict()                        # Set up the delta function for each state.
        for letter in uppercase:
            delta[(0, letter)] = 1
            delta[(4, letter)] = 4
            delta[(6, letter)] = 4
            # Move to putback/error state i.e. State 8/9
            delta[(3, letter)] = 8
            for i in [1,2,7]:
                delta[(i, letter)] = 9
            
        for letter in lowercase:
            delta[(0, letter)] = 2      
            delta[(1, letter)] = 1
            delta[(2, letter)] = 2
            delta[(4, letter)] = 4
            delta[(6, letter)] = 4
            # Move to putback/error state i.e. State 8/9
            delta[(3, letter)] = 8      # e.g. 0a  check
            delta[(7, letter)] = 9      # e.g. ;b  error
            
        for number in numbers:
            delta[(0, number)] = 3
            delta[(3, number)] = 3
            delta[(6, number)] = 4
            # Move to putback/error state i.e. State 8/9
            for i in [1,2]:
                delta[(i, number)] = 8
            delta[(7, number)] = 9      # e.g. ;0 error
        
        for space in whitespace:
            delta[(0, space)] = 0
            for i in [4,6]:
                delta[(i, space)] = 4

        for character in invalids:
            for i in [0,4,5]:
                 delta[(i, character)] = 9
            for i in [1,2,3,6,7]:
                delta[(i, character)] = 8

        delta[(0, '"')], delta[(6, '~')], delta[(6, '"')] = 4,4,4
        delta[(4, '"')] = 5
        delta[(4, '~')] = 6
        delta[(0, ')')], delta[(0, '(')], delta[(0, ';')] = 7,7,7
        self.delta = delta

    def transition_state(self, input):
        if ((self.current_state, input) not in self.delta.keys()):         
            self.current_state = 9
        else:
            self.previous_state = self.current_state
            if self.current_state == 3:
                if self.check_max_int():
                    self.current_state = self.delta[(self.current_state, input)]
                else:
                    self.current_state = 9
            else:
                self.current_state = self.delta[(self.current_state, input)]

            
    def run_char(self, input):
        if(input == '\t' or input == '\n' or input == ' ' or input == '') and self.current_state != 4:
            # If white space and not in string check token
            if self.current_state == 3:
                if self.check_max_int():
                    identifier = self.checkIdentifier(self.current_state)
                    if identifier != "ERROR":
                        self.Trie.proccessWord(self.current_word)
                    self.resetTrackedVariables()
                    return identifier
                else:
                    self.resetTrackedVariables()
                    return "ERROR"
            else:
                identifier = self.checkIdentifier(self.current_state)
                if identifier != "ERROR":
                    self.Trie.proccessWord(self.current_word)
                self.resetTrackedVariables()
                return identifier

        else:
            if not self.putback_bool:
                # if putback is false then change state and check state
                self.transition_state(input)            
                if self.current_state != 8:
                    #if not in putback state then add to current word
                    if input != "~" or self.current_state == 6:
                        self.current_word = self.current_word + input

                else:
                    #  if new state is putback state then set put back char,
                    #  process word and reset
                    self.set_putback(input)
                    identifier = self.checkIdentifier(self.previous_state)
                    self.Trie.proccessWord(self.current_word)
                    self.resetTrackedVariables()
                    return identifier


    def driver(self):
        with self.file as f:
            while True:
                if self.putback_bool:
                    identifier =  self.run_char(self.putback())
                else:
                    c = f.read(1)
                    if not c:
                        break
                    identifier = self.run_char(c)
                if identifier != None:
                    if identifier == 'ID':
                        return '<'+identifier +','+str(self.Trie.checkWordExists(self.previous_word))+'>'
                    elif identifier == 'STRING':
                        word = []
                        for letter in self.previous_word:
                            word.append(letter)
                        return '<' + identifier + ',' + str(word) + '>'
                    elif identifier == 'INT':
                        return '<' + identifier + ',' + self.previous_word + '>'
                    elif identifier == 'LPAR' or identifier == 'RPAR' or identifier == 'SEMICOLON':
                        return '<' + identifier + ', 0 >'
                    elif identifier == 'ERROR':
                        return '<' + identifier + '>'

    def in_accepting_state(self, state):
        return state in self.accepting_states

    def resetTrackedVariables(self):
        self.current_state = 0
        self.previous_word = self.current_word
        self.current_word = ""

    def putback(self):
        self.putback_bool = False
        return self.putback_val

    def set_putback(self, character):
        self.putback_bool = True
        self.putback_val = character

    def checkIdentifier(self, state):
        if self.in_accepting_state(state):      #check if in accepting state
            if state == 1 or state == 2:
                return "ID"
            elif state == 3:
                return "INT"
            elif state == 5:
                return "STRING"
            elif state == 7:
                if self.current_word == '(':
                    return 'LPAR'
                elif self.current_word == ')':
                    return 'RPAR'
                elif self.current_word == ';':
                    return 'SEMICOLON'
        else:
            return "ERROR"

    def check_max_int(self):
        if len(self.current_word) > 5:
            return False
        elif len(self.current_word) == 5:
            if int(self.current_word[0]) > 6:
                return False
            elif int(self.current_word[0]) == 6:
                if int(self.current_word[1]) > 5:
                    return False
                elif int(self.current_word[1]) == 5:
                    if int(self.current_word[2]) > 5:
                        return False
                    elif int(self.current_word[2]) == 5:
                        if int(self.current_word[3]) > 3:
                            return False
                        elif int(self.current_word[3]) == 3:
                            if int(self.current_word[4]) > 4:
                                return False
        return True