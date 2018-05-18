#!/usr/bin/python

import re
import os
import sys
from nltk.tokenize import RegexpTokenizer
from pymongo import *
from bs4 import BeautifulSoup

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
                    self.docCount += 1
                    path = os.path.join(subdir, f)
                    #print(path)
                    parser = Parser(self.tokenDict, path[13:])
                    parser.input(path) 
                    #self.putDatabase(parser.tokenDict, path[13:], parser.totalFreq)
                    self.tokenDict = parser.tokenDict
                    #print(self.tokenDict)

    def tfidf(self):
       # W(t, d) = [1 + log(tftd)] * log(N/dft))
       # df(t) =  number of doc that contain the token 
       # tftd = number of tokens in the doc
               


       return 1.1

    def putDatabase(self, tokenDict, docID, totalFreq):
        for token, freq in tokenDict.items():
            query = {'token': token} 
            postings = {} 
            old_dict = self.Dictionary.find_one(query)
            
            if old_dict != None:
                 postings = old_dict["Postings"]

            postings[docID] =  self.tfidf(freq, tokenDict)
            new_dict = {"token": token, "Postings": postings} 
            self.Dictionary.save(new_dict)

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
            if char.isalnum() and char != u" ":
                word += char
            elif word and word != "": 
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
                
r = Reader()
r.getInput()
print(r.tokenDict)
r.writeFile()
