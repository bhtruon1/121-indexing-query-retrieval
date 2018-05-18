#!/usr/bin/python

import re
import os
import sys
import math
from nltk.tokenize import RegexpTokenizer
from pymongo import *
from bs4 import BeautifulSoup

#format of dictionary: {token : {docID: freq/tfidf}}

class Reader:
    def __init__(self):
        self.tokenDict = {}
        self.rootDir = "WEBPAGES_RAW"
        self.docCount = 0
        #self.Dictionary = Dictionary

    def getInput(self):          
        for subdir, dirs, files in os.walk(self.rootDir):
            for f in files:
                if ".json" not in f and ".tsv" not in f:  
                    path = os.path.join(subdir, f)
                    #print(path)
                    parser = Parser(self.tokenDict, path[13:])
                    parser.input(path) 
                    self.tokenDict = parser.tokenDict
                    self.docCount += 1
                    #print(self.tokenDict)

    def get_number_of_docs(self):
        return self.docCount
 
    def get_number_of_tokens(self):
        return len(self.tokenDict) 
 
    def freq_to_tfidf(self):
       for token in self.tokenDict:
           dft = len(self.tokenDict[token]) 
           for docID in self.tokenDict[token]:
               tftd = self.tokenDict[token][docID] 
               self.tokenDict[token][docID] = self.tfidf(tftd, dft)

    def tfidf(self, tftd, dft):
       # W(t, d) = [1 + log(tftd)] * log(N/dft))
       # dft = number of doc that contain the token 
       # tftd = number of tokens in the doc
       N = self.docCount
       result = (1 + math.log10(tftd)) * math.log10(N/dft)                 
       return result

    def writeFile(self):
        with open("dictionary.txt", "w") as log:
            log.write(str(self.tokenDict))

class Parser:
    def __init__(self, tokenDict, docID):
        self.tokenDict = tokenDict
        self.docID = docID
        self.totalFreq = 0

    def input(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as doc:
                rawHTML = doc.read()
                soup = BeautifulSoup(rawHTML, "html.parser")
                text = soup.find_all(text=True)
                for string in text:
                    self.parseString(string.lower())
        except IOError:
            print("File {} Doesn't Exist".format(path))

    def parseString(self, string):
        #print(string)
        word = u""
        for char in string:
            if char.isalpha() or char.isdigit():
                word += char
            else:
                if word != u"": 
                    self.newWord(word)
                word = ""
                     
    def newWord(self, word):
        try:
            if self.docID in self.tokenDict[word]: 
                self.tokenDict[word][self.docID] += 1
            else:
                self.tokenDict[word][self.docID] = 1
        except KeyError:
            self.tokenDict[word] = {self.docID: 1}
        self.totalFreq += 1
                
