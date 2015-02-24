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
import math

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

            #figure out weights, w = tf * idf / magnitude
            # tf = 1 + log(len(self.index[term][docID])
            # idf = log(N/len(self.index[term]))
            # magnitude = sqrt( sum of squared rawtf)
            # N = number of documents (JEN HELP)
            #CURRENTLY HARD-CODED, WE CAN DO BETTER
            N = 771
            for term in self.index.keys():
                df = len(self.index[term])
                idf = math.log(N/df)
                for docID in self.index[term].keys():
                    tf = len(self.index[term][docID])
                    #putting the weight in the docID list
                    rawW = math.log1p(tf) * idf
                    self.index[term][docID][0] = rawW
                    


            

            
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
            matches2 = []
            for i in range(len(query)):
                if i==0:
                    if query[i] in self.index:
                        for docID in self.index[query[i]]:
                            matches.append(docID)
                            
                else:
                    #for each document that matched the first word
                    #see if the word after it is the next word in the query
                    for docID in matches:
                        for position in self.index[query[i-1]][docID]:
                            if docID not in matches2:
                                if docID in self.index[query[i]]:
                                    for j in range(-5, 5):
                                        if position+j in self.index[query[i]][docID]:
                                            matches2.append(docID)
                                            #don't need to look at other positions
                                            break
            #matches contains docIDs of results
            self.processMatches(matches2)
        except ValueError:
            print("Not a valid near query.")

            

    def phraseQuery(self):
        query = self.getQuery()
        
        matches = []
        matches2 = []
        for i in range(len(query)):
            if i==0:
                if query[i] in self.index:
                    for docID in self.index[query[i]]:
                        matches.append(docID)
            else:
                #for each document that matched the first word
                #see if the word after it is the next word in the query
                
                for docID in matches:
                    for position in self.index[query[i-1]][docID]:
                        if docID in self.index[query[i]]:
                            if position+1 in self.index[query[i]][docID]:
                                matches2.append(docID)
                                #don't look at remaining positions
                                break
        #matches contains docIDs of results
        self.processMatches(matches2)



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
            matches = []
            query.remove("and")
            if len(query) == 2:
                for docID1 in self.index[query[0]]:
                    for docID2 in self.index[query[1]]:
                        if docID1 == docID2:
                            matches.append(docID1)
                            
            
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
