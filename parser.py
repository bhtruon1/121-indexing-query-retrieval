#!/usr/bin/python

class Parser:
    def __init__():
        self.tokenDict = {}
    def input_to_string():
        # turn input html to contentString 
        pass
    def input():
        # get input from RAW WEBSITES
        pass
    def parseString(self, rawInput):
        word = ""
        for char in rawInput:
            if str(char).isalum() and str(char) != "_":
                word += char
            else:
                if  word and word != "_":
                    self.newWord(word)
                word = ""
    def newWord(self, word):
        if word in self.result.key():
            self.result[word] += 1
        else:
            self.result[word] = 1
 
                
        
