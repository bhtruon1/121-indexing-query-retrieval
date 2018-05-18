#!/usr/bin/python

from parser import *
import pickle
import os

#  Verify mongo exists and is running, set up database schema 

#from pymongo import *
#client = MongoClient('localhost', 27017)
#db = client['InvertedIndex']
#Dictionary = db["Dictionary"]
#Dictionary.create_index([("token", ASCENDING)])

# tokenInfo = {"token": "Ben", "Postings": {"doc1": 3.2, "doc2": 4}} 
# token_id = Dictionary.insert(tokenInfo) 
# print(Dictionary.find_one())

def save_analytics(r):
  with open("analytics.txt", "w") as log:
      log.write("Number of documents of the corpus: {}\n".format(r.get_number_of_docs()))
      log.write("Number of tokens present in index: {}\n".format(r.get_number_of_tokens()))
      log.write("The total size (in KB) of index of disk: {}".format(os.path.getsize("save.p")/1000))

def save_pickleFile():
    r = Reader()
    r.getInput()
    r.freq_to_tfidf()
    #print(r.tokenDict)
    pickle.dump(r.tokenDict, open("save.p", "wb"))
    save_analytics(r) 

save_pickleFile() 
