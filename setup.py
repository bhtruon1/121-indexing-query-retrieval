#!/usr/bin/python

from pymongo import *
from bs4 import BeautifulSoup

#  Verify mongo exists and is running, set up database schema 

client = MongoClient('localhost', 27017)
db = client['InvertedIndex']
Dictionary = db["Dictionary"]
Dictionary.create_index([("token", ASCENDING)])

# tokenInfo = {"token": "Ben", "Postings": {"doc1": 3.2, "doc2": 4}} 
# token_id = Dictionary.insert(tokenInfo) 
# print(Dictionary.find_one())


