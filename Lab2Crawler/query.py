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
        self.cache = webdb.WebDB(cache)
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
                for i in range(len(fileTokens)):
                    fileTokens[i] = fileTokens[i].replace('\n', '')
                
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


    def nearQuery(self):
        query = self.getQuery()
        try:
            query.remove("near")
            matches = []
            for i in range(len(query)):
                if i==0:
                    if query[i] in self.index:
                        for docID in self.index[query[i]]:
                            matches.append(docID)
                else:
                    #for each document that matched the first word
                    #see if the word after it is the next word in the query
                    isNear = False
                    for match in matches:
                        for position in self.index[query[i-1]][docID]:
                            if docID in self.index[query[i]]:
                                for j in range(-5, 5):
                                    if position+j in self.index[query[i]][docID]:
                                        isNear = True
                        if not isNear:
                            matches.remove(match)
            #matches contains docIDs of results
            self.processMatches(matches)
        except ValueError:
            print("Not a valid near query.")

            

    def phraseQuery(self):
        query = self.getQuery()
        
        matches = []
        for i in range(len(query)):
            if i==0:
                if query[i] in self.index:
                    for docID in self.index[query[i]]:
                        matches.append(docID)
            else:
                #for each document that matched the first word
                #see if the word after it is the next word in the query
                isPhrase = False
                for match in matches:
                    for position in self.index[query[i-1]][docID]:
                        if docID in self.index[query[i]]:
                            if position+1 in self.index[query[i]][docID]:
                                isPhrase = True
                    if not isPhrase:
                        matches.remove(match)
        #matches contains docIDs of results
        self.processMatches(matches)



    def booleanOR(self):
        query = self.getQuery()
        try: 
            query.remove("or")
            matches = []
            for i in range(len(query)):
                if query[i] in self.index:
                    for docID in self.index[query[i]]:
                        if docID not in matches:
                            matches.append(docID)
        
            self.processMatches(matches)
        except ValueError:
            print("Not a valid OR query.")

    def booleanAND(self):
        query = self.getQuery()
        try: 
            query.remove("and")
            matches = []
            for i in range(len(query)):
                if i==0:
                    if query[i] in self.index:
                        for docID in self.index[query[i]]:
                            matches.append(docID)
                else:
                    #for each document that matched the first word
                    #see if the word after it is the next word in the query
                    isInBoth = False
                    for docID in matches:
                        if docID in self.index[query[i]]:
                            isInBoth = True
                    if not isInBoth:
                        matches.remove(match)
            #matches contains docIDs of results
            self.processMatches(matches)
        except ValueError:
            print("Not a valid AND query.")
            

    def singleToken(self):
        query = self.getQuery()
        #make sure users only enter one word.
        if len(query) != 1:
            print("Invalid single token query.")
        else:
            matches = []
            if query[0] in self.index.keys():
                for docID in self.index[query[0]]:
                    matches.append(docID)
        #matches contains docIDs of results
        self.processMatches(matches)

    def processMatches(self, matches):
        print("Results:", len(matches))
        
        nameDict = {}
        for docID in matches:
            itemID = self.cache.lookupItemIDFromDocID(int(docID))
            name = self.cache.lookupItemName(itemID)
            if name in nameDict.keys():
                nameDict[name] += 1
            else:
                nameDict[name] = 0
        numHits = list(nameDict.values())
        names = list(nameDict.keys())
        mostCommon = names[numHits.index(max(numHits))]
        print(mostCommon, "(", nameDict[mostCommon], ")")



    def getQuery(self):
        query = input("Enter query: ")
        query = query.split()
        query = self.spider.stem(self.spider.lower(query))
        return query

def main():
    bse = BooleanSearchEngine("data/clean/", "data/cache.db", "data/index.p")
    
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
            bse.booleanAND()
        elif search == "3":
            bse.booleanOR()
        elif search == "4":
            bse.phraseQuery()
        elif search == "5":
            bse.nearQuery()
        elif search != "0":
            print("Invalid input.")
    print("Goodbye")

main()
