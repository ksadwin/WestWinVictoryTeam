"""
Kelly Sadwin
490 Lab 3, due 2/20/15
Using the database created in Lab 2, returns pages that match:
 1. a single token query
 2. a boolean AND query
 3. a boolean OR query
 4. a phrase query
 5. a NEAR query
"""
import webdb
import os, sys
from spider import *
import pickle

class BooleanSearchEngine():
    def __init__(self, dirLocation, cache, picklePlace):
        self.cache = cache
        self.dir = dirLocation
        self.spider = Spider()
        #search for pickled index
        if os.path.exists(picklePlace):
            self.index = pickle.load(open(picklePlace, "rb"))
        else:
            #create index
            self.index = {}
            #index will be a multidimensional structure
            # 1. a dictionary (terms as keys)
            # 2. of dictionaries (values mapped to terms are docIDs as keys)
            # 3. of lists (values mapped to docIDs are lists of positions)

            #go through each clean file and tokenize
            for filename in os.listdir(self.dir):
                docID = os.path.splitext(filename)[0]
                fileTokens = open(self.dir+filename, "r", encoding="utf-8").readlines()
                terms = self.spider.stem(self.spider.lower(fileTokens))
                
                #check if all of the tokens are already in the dictionary
                for position in range(len(terms)):
                    #check if the term is in the dictionary of terms
                    if terms[position] not in self.index.keys():
                        #add term to dictionary, then put docID:positionList in secondary dict
                        self.index[terms[position]] = {docID:[position]}
                    elif docID not in self.index[terms[position]].keys():
                        #add docID:positionList dictionary to term's dictionary
                        self.index[terms[position]][docID] = [position]
                    else:
                        #add position to docID's list
                        self.index[terms[position]][docID].append(position)

            
            pickle.dump(self.index, open("data/index.p", "wb"))


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




    def phraseQuery(self):
        query = getQuery()
        
        matches = []
        for i in range(len(query)):
            if i==0:
                if query[i] in self.index:
                    for docID in self.index[query[i]]:
                        matches.append(docID)
            else:
                isPhrase = False
                #for each document that matched the first word
                #see if the word after it is the next word in the query



    def booleanOR(self):
        query = getQuery()
        grossMatches = []
        for i in range(len(query)):
            individualMatches = []
            if query[i] is not "or":
                if query[i] in self.index:
                    for docID in self.index[query[i]]:
                        grossMatches.append(docID)
        #grossMatches contains docIDs of results

    def booleanAND(self):
        query = getQuery()
        grossMatches = []
        listOfIM = []
        for i in range(len(query)):
            individualMatches = []
            if query[i] is not "and":
                if query[i] in self.index:
                    for docID in self.index[query[i]]:
                        grossMatches.append(docID)
                        individualMatches.append(docID)
            listOfIM.append(individualMatches)
        for word in grossMatches:
            isCommon = True
            for l in listOfIM:
                if word not in l:
                    isCommon = False
            if not isCommon:
                grossMatches.remove(word)
        #grossMatches contains docIDs of results
            

    def singleToken(self):
        query = getQuery()
        #make sure users only enter one word.
        if len(query) != 1:
            print("Invalid single token query.")
        else:
            matches = []
            if query[0] in self.index:
                for docID in self.index[query[0]]:
                    matches.append(docID)
        #matches contains docIDs of results

def getQuery():
    query = input("Enter query: ")
    query = query.split()
    query = self.spider.stem(self.spider.lower(query))
    return query

def main():
    bse = BooleanSearchEngine("data/clean/", "data/cache.db", "data/index.p")

    #bse.printIndex()
    
    #a while loop for getting user queries
    search = ""
    while search != "0":
        print(" 1. single token query")
        print(" 2. AND query")
        print(" 3. OR query")
        print(" 4. phrase query")
        print(" 5. NEAR query")
        search = input("Enter number for search type, or 0 to quit: ")
        if search == "1":
            bse.singleToken()
        elif search == "2":
            print("AND")
        elif search == "3":
            print("OR")
        elif search == "4":
            print("phrase")
        elif search == "5":
            print("NEAR")
        elif search != "0":
            print("Invalid input.")
    print("Goodbye")

main()
