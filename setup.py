#!/usr/bin/python

from parser import *
import pickle


def construct_and_pickle_index():
    print("Constructing index...")
    r = Reader("WEBPAGES_RAW")
    tokenDict = r.constructIndex()

    print("Pickling index...")
    try:
        pickle.dump(tokenDict, open("save.p", "wb"))
    except:
        print("Pickle unsuccessful.")

    print("Writing analytics...")
    r.saveAnalytics()

