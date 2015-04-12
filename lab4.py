"""
Lab 4: Ranked Retrieval
Kelly Sadwin & Jen Westling
Uses different weighting systems (nnn or ltc) for
documents and queries to perform ranked retrieval.
Inherits SearchEngine class from a file currently called query.py
"""
from query import SearchEngine
import math
import os
import pickle

class RankedSearchEngine(SearchEngine):

    def __init__(self, dirLocation, cache, nnnp, ltcp):
        SearchEngine.__init__(self, dirLocation, cache, nnnp)
        if os.path.exists(ltcp):
            print("Loading ltc index...")
            self.ltcindex = pickle.load(open(ltcp, "rb"))
        else:
            print("Creating new ltc index...")
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



    def scoreDocs(self, query, useLTC = True):
        score = {}
        itemScore = {}
        for term in query.keys():
            if useLTC:
                #doc ltc
                if term not in self.ltcindex.keys():
                    continue
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
                if term not in self.index.keys():
                    continue
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


        return score, itemScore



    def processMatches(self, score, itemScore):
        docIDs = sorted(score, key=score.get, reverse=True)
        itemIDs = sorted(itemScore, key=itemScore.get, reverse=True)
        count = 1
        for item in itemIDs:
            print(count, ")", item, "\tScore:", itemScore[item])
            count += 1
            if count > 5:
                break
        print("\n")
        count = 1
        for docID in docIDs:
            rslt = self.cache.lookupCachedURL_byID(int(docID))
            print(count, ")", rslt[2], "\n", rslt[0])
            print("Score:", score[docID], "\n")
            count += 1
            if count > 5:
                break


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




    def menu(self):
        search = ""
        while search != "n":
            d = input("For documents: nnn or ltc?: ")
            q = input("For queries: nnn or ltc?: ")
            if q == "ltc":
                query = self.getLTCQuery()
            else:
                query = self.getNNNQuery()
            if d == "ltc":
                docIDs, itemIDs = self.scoreDocs(query)
                self.processMatches(docIDs, itemIDs)
            else:
                docIDs, itemIDs = self.scoreDocs(query, False)
                self.processMatches(docIDs, itemIDs)
            search = input("Continue? y/n: ")



def main():
    rse = RankedSearchEngine("data/clean/", "data/cache.db", "data/nnnindex.p", "data/ltcindex.p")
    rse.menu()

if __name__ == "__main__":
   main()
