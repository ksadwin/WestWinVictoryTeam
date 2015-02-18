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

class BooleanSearchEngine():
    def __init__(self, dirLocation, cache):
        self.cache = cache
        self.dir = dirLocation

        #create index
        #index will be a multidimensional structure
        # 1. dictionary (keys = terms)
        # 2. of dictionaries (keys = docIDs)
        # 3. of lists (value pair for each docID, all positions of words)

        #I wrote this two ways, maybe one of them will make sense
        # 1. keys of termDict: unique terms
        # 2. each unique term is mapped to dict of docIDs containing term
        # 3. each docID is mapped to a list of positions where term is found
        self.termDict = {}
        spider = Spider()
        #go through each clean file and tokenize
        for filename in os.listdir(self.dir):
            docID = os.path.splitext(filename)[0]
            fileTokens = open(self.dir+filename, "r", encoding="utf-8").readlines()
            terms = spider.stem(spider.lower(fileTokens))
            
            #check if all of the tokens are already in the dictionary
            for position in range(len(terms)):
                #check if the term is in the dictionary of terms
                if terms[position] not in self.termDict.keys():
                    #add term to dictionary, then put docID:positionList in secondary dict
                    self.termDict[terms[position]] = {docID:[position]}
                elif docID not in self.termDict[terms[position]].keys():
                    #add docID:positionList dictionary to term's dictionary
                    self.termDict[terms[position]] = ({docID:[position]})
                else:
                    #add position to docID's list
                    self.termDict[terms[position]][docID].append(position)

        #now pickle it??
        """
        Prints out index
        for term in self.termDict.keys():
            print(term)
            for docID in self.termDict[term]:
                print(docID, end=":\t")
                for position in self.termDict[term][docID]:
                    print(position, end=" ")
                print()
            print()
        """

    def phraseQuery(self):
        query = getQuery()
        query = spider.stem(spider.lower(q))
        matches = []
        for i in range(len(query)):
            if i==0:
                if query[i] in self.termDict:
                    for docID in self.termDict[query[i]]:
                        matches.append(docID)
            else:
                isPhrase = False
                #for each document that matched the first word
                #see if the word after it is the next word in the query
                
                

    def booleanOR(self):
        query = getQuery()
        query = spider.stem(spider.lower(q))
        grossMatches = []
        for i in range(len(query)):
            individualMatches = []
            if query[i] is not "or":
                if query[i] in self.termDict:
                    for docID in self.termDict[query[i]]:
                        grossMatches.append(docID)
        #grossMatches contains docIDs of results

    def booleanAND(self):
        query = getQuery()
        query = spider.stem(spider.lower(q))
        grossMatches = []
        listOfIM = []
        for i in range(len(query)):
            individualMatches = []
            if query[i] is not "and":
                if query[i] in self.termDict:
                    for docID in self.termDict[query[i]]:
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
            query = spider.stem(spider.lower(query))
            if query[0] in self.termDict:
                for docID in self.termDict[query[0]]:
                    matches.append(docID)
        #matches contains docIDs of results

def getQuery():
    query = input("Enter query: ")
    query = query.split()
    return query

def main():
    bse = BooleanSearchEngine("data/clean/", "data/cache.db")
    
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
