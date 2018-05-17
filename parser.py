#!/usr/bin/python

import re
import os
import sys
from bs4 import BeautifulSoup

class Reader:
    def __init__(self):
        self.docDict = {}
        self.rootDir = "WEBPAGES_RAW"

    def getInput(self):          
        for subdir, dirs, files in os.walk(self.rootDir):
            for f in files:
                if ".json" not in f and ".tsv" not in f:  
                    path = os.path.join(subdir, f)
                    parser = Parser()
                    parser.input(path) 
                    self.docDict[path] = parser.tokenDict #placeholder for db

class Parser:
    def __init__(self):
        self.tokenDict = {}

    def input(self, path):
        try:
            doc = open(path, 'r')
            rawHTML = doc.read()
            soup = BeautifulSoup(rawHTML, "lxml")
            text = soup.find_all(text=True)
            for string in text:
                self.parseString(string)
        except IOError:
            print("File {} Doesn't Exist".format(path))


    def parseString(self, string):
        word = u""
        for char in string:
            if char.isalnum() and char != u"_":
                word += char
            else:
                if  word and u"_" not in word:
                    self.newWord(word)
                word = u""

    def newWord(self, word):
        if word in self.tokenDict.keys():
            self.tokenDict[word] += 1
        else:
            self.tokenDict[word] = 1
 
                
r = Reader()
r.getInput()
print(r.docDict)
