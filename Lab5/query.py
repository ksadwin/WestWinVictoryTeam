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
from Lab5 import webdb
from Lab5 import spider
import os, sys
import pickle
import math
import lab5
import string

class BooleanSearchEngine():
    def __init__(self, dirLocation, cache, nnnp, ltcp):
        self.cache = webdb.WebDB(cache)
        self.dir = dirLocation
        self.spider = spider.Spider()
        #It's not hardcoded anymore, Kelly!
        self.N = self.cache.countURLs()
        #search for pickled index
        if os.path.exists(nnnp) and os.path.exists(ltcp):
            print("Loading data...")
            self.index = pickle.load(open(nnnp, "rb"))
            self.ltcindex = pickle.load(open(ltcp, "rb"))
        else:
            print("Creating new nnn index...")
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
            print("nnn index created. Saving...")
            pickle.dump(self.index, open("data/nnnindex.p", "wb"))

            print("nnn index saved.\nCreating new ltc index...")

            
            #figure out weights, w = tf * idf / magnitude
            # tf = 1 + log(len(self.index[term][docID])-1)
            # idf = log(N/len(self.index[term]))
            # magnitude = sqrt( sum of squared rawW )
            
            #accessing the correct indices: turn docID into int, subtract 1
            sqrdMag = [0] * self.N
            self.ltcindex = self.index.copy()
            for term in self.ltcindex.keys():
                df = len(self.ltcindex[term])
                idf = math.log(self.N/df)
                for docID in self.ltcindex[term].keys():
                    #subtract one to account for extra idx in beginning
                    tf = len(self.ltcindex[term][docID])-1
                    #wt = tf * idf
                    rawW = math.log1p(tf) * idf
                    self.ltcindex[term][docID][0] = rawW
                    sqrdMag[int(docID)-1] += math.pow(rawW, 2)

            for term in self.ltcindex.keys():
                for docID in self.ltcindex[term].keys():
                    self.ltcindex[term][docID][0] /= math.sqrt(sqrdMag[int(docID)-1])
            print("ltc index created. Saving...")
            pickle.dump(self.ltcindex, open("data/ltcindex.p", "wb"))
            print("ltc index saved.")


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






    def scoreDocs(self, query, useLTC = True, rq = ""):
        score = {}
        itemScore = {}
        for term in query.keys():
            if useLTC:
                #doc ltc
                for docID in self.ltcindex[term]:
                    if docID not in score.keys():
                        score[docID] = self.ltcindex[term][docID][0]*query[term]
                    else:
                        score[docID] += self.ltcindex[term][docID][0]*query[term]
                    itemID = self.cache.lookupItemIDFromDocID(int(docID))
                    item = self.cache.lookupItemName(int(itemID))
                    if item not in itemScore.keys():
                        itemScore[item] = self.ltcindex[term][docID][0]*query[term]
                    else:
                        itemScore[item] += self.ltcindex[term][docID][0]*query[term]
            else:
                #doc nnn
                for docID in self.index[term]:
                    if docID not in score.keys():
                        score[docID] = len(self.index[term][docID])*query[term]
                    else:
                        score[docID] += len(self.index[term][docID])*query[term]
                    itemID = self.cache.lookupItemIDFromDocID(int(docID))
                    item = self.cache.lookupItemName(int(itemID))
                    if item not in itemScore.keys():
                        itemScore[item] = len(self.index[term][docID])*query[term]
                    else:
                        itemScore[item] += len(self.index[term][docID])*query[term]

        #lab 5 additions
        sortedDocIDs = sorted(score, key=score.get, reverse=True)
        
        rslts, R = self.translateResults(rq, sortedDocIDs)
        #TODO: add other precision tests
        print("AUC:", lab5.auc(rslts, R))

        """
        count = 1
        for item in sorted(itemScore, key=itemScore.get, reverse=True):
            print(count, ")", item, "\tScore:", itemScore[item])
            count += 1
            if count > 5:
                break
        print("\n")
        count = 1
        sortedDocIDs = sorted(score, key=score.get, reverse=True)
        for docID in sortedDocIDs:
            rslt = self.cache.lookupCachedURL_byID(int(docID))
            print(count, ")", rslt[2], "\n", rslt[0])
            print("Score:", score[docID], "\n")
            count += 1
            if count < 5:
                break
        """


    def getNNNQuery(self, q = ""):
        query = {}
        #get tf for terms in query
        for term in self.getQuery(q):
            if term not in query.keys():
                query[term] = 1
            else:
                query[term] += 1
        return query

    
    def getLTCQuery(self, q = ""):
        query = self.getNNNQuery(q)
        #get weights and squared magnitude
        sqMag = 0
        for term in query.keys():
            if term in self.ltcindex.keys():
                df = len(self.ltcindex[term])
                idf = math.log(self.N/df)
                tf = math.log1p(query[term])
                query[term] = tf * idf
                sqMag += math.pow(query[term], 2)
                
        #normalize
        for term in query.keys():
            query[term] = query[term]/math.sqrt(sqMag)
        return query
        
    def getQuery(self, query = ""):
        if query == "":
            query = input("Enter query: ")
        query = query.translate(query.maketrans("", "", string.punctuation))
        query = query.split()
        query = self.spider.stem(self.spider.lower(query))
        return query

    def translateResults(self, item, results):
        """
        Finds number R of relevant webpages for a given item.
        Also processes results into true/false list.
        Returns a tuple booleanRslts, R
        """
        booleanRslts = []
        R = 0
        #results is a list of docIDs
        for docID in results:
            itemID = self.cache.lookupItemIDFromDocID(int(docID))
            if self.cache.lookupItemName(itemID) == item:
                booleanRslts.append(True)
                R += 1
            else:
                booleanRslts.append(False)

        #Print to test that numbers are making sense.
        print(item, "has", R, "out of", self.N, "results.")

        return booleanRslts, R

def main():
    bse = BooleanSearchEngine("data/clean/", "data/cache.db", "data/nnnindex.p", "data/ltcindex.p")


    queries = lab5.getQueries()
    for q in queries:
        print(q)
        nnnq = bse.getNNNQuery(q)
        ltcq = bse.getLTCQuery(q)
        print("nnn.nnn")
        bse.scoreDocs(nnnq, False, q)
        print("nnn.ltc")
        bse.scoreDocs(nnnq, True, q)
        print("ltc.nnn")
        bse.scoreDocs(ltcq, False, q)
        print("ltc.ltc")
        bse.scoreDocs(ltcq, True, q)
        print("Random")
        rslts = lab5.randomResult(bse.N)
        #rslts, R = bse.translateResults(q, rslts)
        #all precision tests
        

    
    
    #a while loop for weighted queries
    """
    search = ""
    while search != "n":
        d = input("For documents: nnn or ltc?: ")
        q = input("For queries: nnn or ltc?: ")
        if q == "ltc":
            query = bse.getLTCQuery()
        else:
            query = bse.getNNNQuery()
        if d == "ltc":
            bse.scoreDocs(query)
        else:
            bse.scoreDocs(query, False)
        search = input("Continue? y/n: ")
    """     
    
    #a while loop for getting user queries for BOOLEAN RETRIEVAL
    """
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
    """

main()
