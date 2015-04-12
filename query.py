"""
Kelly Sadwin & Jen Westling
Establishes the SearchEngine class, which functions more as an interface than
a standalone class.
"""
import webdb
import os, sys
from spider import *
import pickle
import math
import string

class SearchEngine():
    def __init__(self, dirLocation, cache, nnnp):
        self.cache = webdb.WebDB(cache)
        self.dir = dirLocation
        self.spider = Spider()
        self.N = self.cache.countURLs()
        #search for pickled index
        if os.path.exists(nnnp):
            print("Loading index...")
            self.index = pickle.load(open(nnnp, "rb"))
        else:
            print("Creating new index...")
            #create index
            self.index = {}
            #index will be a multidimensional structure
            # 1. a dictionary (terms as keys)
            # 2. of dictionaries (values mapped to terms are docIDs as keys)
            # 3. of lists (values mapped to docIDs are lists of positions)

            #this serves as nnn index
            # tf = len(self.index[term][docID]) (the -1 is inconsequential because it is part of a linear function)
            # df = 1
            # w = tf * df = tf

            #go through each clean file and tokenize
            for filename in os.listdir(self.dir):
                docID = os.path.splitext(filename)[0]
                fileTokens = open(self.dir+filename, "r", encoding="utf-8").readlines()
                for i in range(len(fileTokens)):
                    fileTokens[i] = fileTokens[i].replace('\n', '')
                
                terms = self.spider.stem(self.spider.lower(fileTokens))
                
                #check if all of the tokens are already in the dictionary
                for position in range(len(terms)):
                    #check if the current term is in the dictionary of terms
                    if terms[position] not in self.index.keys():
                        #add term to dictionary, then put docID:positionList in secondary dict
                        self.index[terms[position]] = {docID:[0, position]}
                        #first position will be filled with the weight
                    elif docID not in self.index[terms[position]].keys():
                        #add docID:positionList dictionary to term's dictionary
                        self.index[terms[position]][docID] = [0, position]
                        #first position will be filled with the weight
                    else:
                        #add position to docID's list
                        self.index[terms[position]][docID].append(position)
            print("Index created. Saving...")
            pickle.dump(self.index, open("data/nnnindex.p", "wb"))

            print("Index saved.")

            
            


    def printIndex(self):
        #For testing: prints out index
        for term in self.index.keys():
            print(term)
            for docID in self.index[term]:
                print(docID, end=":\t")
                for position in self.index[term][docID]:
                    print(position, end=" ")
                print()
            print() 



    def processMatches(self, matches):
        print("Results:", len(matches))
        if len(matches) != 0:
            nameDict = {}
            for docID in matches:
                itemID = self.cache.lookupItemIDFromDocID(int(docID))
                name = self.cache.lookupItemName(itemID)
                if name in nameDict.keys():
                    nameDict[name] += 1
                else:
                    nameDict[name] = 1
            numHits = list(nameDict.values())
            names = list(nameDict.keys())
            mostCommon = names[numHits.index(max(numHits))]
            print(mostCommon, "(", nameDict[mostCommon], ")")










        
    def getQuery(self, query = ""):
        if query == "":
            query = input("Enter query: ")
        query = query.translate(query.maketrans("", "", string.punctuation))
        #print(query)
        query = query.split()
        query = self.spider.stem(self.spider.lower(query))
        return query




