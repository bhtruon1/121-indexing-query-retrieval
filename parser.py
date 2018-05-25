#!/usr/bin/python

import os
import sys
import math
from bs4 import BeautifulSoup
from collections import defaultdict
# format of dictionary: {token : {docID: freq/tfidf}}

debugging = True

def return_dd_int():
    # Required to allow pickling of nested defaultdict.
    return defaultdict(int)

class Reader:
    # Finds all non-json and non-tsv files in root dir and 
    # uses Parser to create a tokenDict of the form: 
    # {token -> {docID -> tf-idf}}. 
    def __init__(self, rootDir="WEBPAGES_RAW"):
        self.tokenDict = defaultdict(return_dd_int)
        self.rootDir = rootDir
        self.docCount = 0
        self.tokensProcessed = 0

    def constructIndex(self): # -> tokenDict
        print("Beginning to parse all files...")
        self.parseAllFiles()

        print("Converting frequencies to tfidf...")
        self.convert_freq_to_tfidf()

        return self.tokenDict

    def parseAllFiles(self) -> None:
        parser = Parser(self.tokenDict)
        for subdir, dirs, files in os.walk(self.rootDir):
            for f in files:
                if (".json" not in f) and (".tsv" not in f):  
                    path = os.path.join(subdir, f)
                    parser.parseFile(path)
                    self.docCount += 1
                    if debugging:
                        print(path)
        self.tokensProcessed = parser.getTokensProcessed()

    def saveAnalytics(self, filename="analytics.txt") -> None:
        with open(filename, "w") as log:
            log.write("Number of documents of the corpus: {}\n".format(self.get_number_of_docs()))
            log.write("Number of words processed while constructing index: {}\n".format(self.tokensProcessed))
            log.write("Number of tokens present in index: {}\n".format(self.get_number_of_tokens()))
            log.write("The total size (in KB) of index of disk: {}".format(os.path.getsize("save.p")/1000))

    def get_number_of_docs(self) -> int:
        return self.docCount
 
    def get_number_of_tokens(self) -> int: 
        return len(self.tokenDict) 
 
    def convert_freq_to_tfidf(self) -> None: 
        # Replaces frequency count in the tokenDict (docID -> freq) with tf-idf.
        for token in self.tokenDict:
            dft = len(self.tokenDict[token]) 
            for docID in self.tokenDict[token]:
                tftd = self.tokenDict[token][docID] 
                self.tokenDict[token][docID] = self.tfidf(tftd, dft)

    def tfidf(self, tftd, dft) -> float: 
       # W(t, d) = [1 + log(tftd)] * log(N/dft))
       # dft = number of doc that contain the token 
       # tftd = number of tokens in the doc
       N = self.docCount
       result = (1 + math.log10(tftd)) * math.log10(N/dft)                 
       return result

    def writeFile(self) -> None:
        with open("dictionary.txt", "w") as log:
            log.write(str(self.tokenDict))

class Parser:
    def __init__(self, tokenDict) -> None:
        self.tokenDict = tokenDict
        self.tokensProcessed = 0

    def parseFile(self, path) -> None: 
        docID = path[13:]
        text = self.htmlFileToString(path)
        if(text == None):
            return

        for word in self.gen_tokens_from_string(text.lower()):
            self.tokenDict[word][docID] += 1
            self.tokensProcessed += 1

    def htmlFileToString(self, path) -> str: 
        # Opens file and parses plaintext from html tags
        try:
            with open(path, 'r', encoding='utf-8') as doc:
                rawHTML = doc.read()
                soup = BeautifulSoup(rawHTML, "html.parser")
                text = soup.get_text()
                # print(text)
                return text.lower()
        except IOError:
            print("File {} Doesn't Exist".format(path))

    def gen_tokens_from_string(self, string) -> str: 
        # Generator yielding each word from the string
        word = u""
        for char in string:
            if char.isalpha(): # or char.isdigit():
                word += char
            else:
                if word != u"": 
                    yield word
                word = u""
        if word != u"":
            yield word

    def getTokensProcessed(self) -> int:
        return self.tokensProcessed
