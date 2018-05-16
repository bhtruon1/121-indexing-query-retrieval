#!/usr/bin/python

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
                path = os.path.join(subdir, f)
                parser = Parser()
                parser.input(path) 
                self.docDict[path] = parser.tokenDict #placeholder for db

class Parser:
    def __init__(self):
        self.tokenDict = {}

    def input(self, path):
        try:
            print(path)
            doc = open(path, 'r')
            rawHTML = doc.read()
            soup = BeautifulSoup(rawHTML, "lxml", text=True)
        except IOError:
            print("File {} Doesn't Exist".format(path))


    def parseString(self, string):
        word = ""
        for char in string:
            if str(char).isalnum() and str(char) != "_":
                word += char
            else:
                if  word and word != "_":
                    self.newWord(word)
                word = ""

    def newWord(self, word):
        if word in self.tokenDict.keys():
            self.tokenDict[word] += 1
        else:
            self.tokenDict[word] = 1
 
                
r = Reader()
r.getInput()
