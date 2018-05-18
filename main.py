#!/usr/bin/python

import pickle

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

def main():
    print("Type [quit] or [q] to quit")
    print("Type a Query to search")
    result = input("Query: ")
    result = result.lower()
    if result == "quit" or result == "q":
        return
    else:
        try:
            limit = input("Limit Results to 10 ([yes] or [no]): ")
            path = dictionary[result]
            i = 10

            if limit.lower() == "no" or limit.lower() == "n":
                i = len(path) + 1
            
            counter = 0    
            for key in path:
                if counter > i:
                    break  
                print(bookkeeping[key])
                counter += 1

        except KeyError:
            print("{} not found".format(result))
        main()

dictionary = pickle.load(open( "save.p", "rb" ))
bookkeeping = tsv_to_urls()
main()

