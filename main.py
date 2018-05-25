#!/usr/bin/python

import pickle
import operator
import os
from setup import construct_and_pickle_index

def tsv_to_urls():
    bookkeeping = {}
    with open("WEBPAGES_RAW/bookkeeping.tsv", "r") as log:
        for line in log:
            split = line.split()
            key = split[0]
            value = split[1] 
            for i in split[2:]:
                value += i
            bookkeeping[key] = value
    return bookkeeping 

def singleWordQuery(string, limit):
    path = dictionary[string]
    printResults(path, limit)

def multipleWordQuery(result, limit):
    paths = []
    for string in result:
        path = dictionary[string]
        paths.append(path)
    docIDs = set()
    for d in paths:
        docIDs = docIDs.intersection(d)
    path = dict()
    for docID in docIDs:
        tfidf = 0
        for d in paths:
            tfidf += d[docID]
        path[docID] = tfidf
    printResults(path, limit)

def printResults(path, limit):
    i = 10
    if limit.lower() == "no" or limit.lower() == "n":
        i = len(path) + 1
    counter = 0
    sorted_path = sorted(path.items(), key=operator.itemgetter(1), reverse=True)
    for key in sorted_path:
        if counter >= i:
            break
        print(bookkeeping[key[0]])
        counter += 1

def splitWords(string, limit):
    word = ""
    result = []
    for char in string:
        if char.isalpha(): #or char.isdigit():
                word += char
        else:
            if word != "": 
                result.append(word)
            word = ""
    if word != "":
        result.append(word)
    if len(result) != 1:
        multipleWordQuery(result, limit)
    singleWordQuery(result[0], limit)

def main():
    print("Type [quit] or [q] to quit")
    print("Type a Query to search")
    result = input("Query: ")
    result = result.lower()
    if result == "quit" or result == "q":
        return
    else:
        limit = input("Limit Results to 10 (yes or no): ")
        try:
            splitWords(result, limit)
        except KeyError:
            print("{} not found".format(result))
        main()

if __name__ == "__main__":
    if(not os.path.isfile("save.p")):
        construct_and_pickle_index()

    dictionary = pickle.load(open( "save.p", "rb" ))
    bookkeeping = tsv_to_urls()
    main()
