"""
Lab 5: Evaluation
Jen Westling & Kelly Sadwin
"""

import os
import webdb
import random
from lab4 import RankedSearchEngine

class EvaluationEngine(RankedSearchEngine):

    def __init__(self, dirLocation, cache, nnnp, ltcp):
        RankedSearchEngine.__init__(self, dirLocation, cache, nnnp, ltcp)


    def translateResults(self, item, score):
        """
        Finds number R of relevant webpages for a given item.
        Also processes results into true/false list.
        Returns a tuple booleanRslts, R
        """
        booleanRslts = []
        R = 0
        results = sorted(score, key=score.get, reverse=True)
        for docID in results:
            itemID = self.cache.lookupItemIDFromDocID(int(docID))
            if self.cache.lookupItemName(itemID) == item:
                booleanRslts.append(True)
                R += 1
            else:
                booleanRslts.append(False)
        return booleanRslts, R



    def evaluate(self):
        pa10 = [0] *5
        par = [0] *5
        ap = [0] *5
        auc = [0] *5
        #for each of the three item types
        path = "data/item/"
        types = os.listdir(path)
        numqueries = 0
        for t in types:
            f = open(path+t, "r")
            #for each item in the file
            for line in f.readlines():
                numqueries += 1
                q = line.strip("\n")
                if q == "Pirates of the Caribbean: Dead Man's Chest":
                    continue
                print(q)
                nnnq = self.getNNNQuery(q)
                ltcq = self.getLTCQuery(q)

                t = t.strip(".txt")
                itemID = self.cache.lookupItem(q, t)
                R = self.cache.getItemRVal(itemID)
                
                #nnn.nnn
                docIDs = self.scoreDocs(nnnq, False)[0]
                rslts, numTrue = self.translateResults(q, docIDs)
                for i in range(R-numTrue):
                    rslts.append(True)
                for i in range(self.N - len(rslts)):
                    rslts.append(False)
                evaluateScores(pa10, par, ap, auc, 0, rslts, R)

                #ltc.nnn
                docIDs = self.scoreDocs(nnnq)[0]
                rslts, numTrue = self.translateResults(q, docIDs)
                for i in range(R-numTrue):
                    rslts.append(True)
                for i in range(self.N - len(rslts)):
                    rslts.append(False)
                evaluateScores(pa10, par, ap, auc, 1, rslts, R)

                #nnn.ltc
                docIDs = self.scoreDocs(ltcq, False)[0]
                rslts, numTrue = self.translateResults(q, docIDs)
                for i in range(R-numTrue):
                    rslts.append(True)
                
                for i in range(self.N - len(rslts)):
                    rslts.append(False)
                evaluateScores(pa10, par, ap, auc, 2, rslts, R)

                #ltc.ltc
                docIDs = self.scoreDocs(ltcq)[0]
                rslts, numTrue = self.translateResults(q, docIDs)
                for i in range(R-numTrue):
                    rslts.append(True)
                for i in range(self.N - len(rslts)):
                    rslts.append(False)
                evaluateScores(pa10, par, ap, auc, 3, rslts, R)

                #random results
                rslts = randomResult(self.N, R)
                evaluateScores(pa10, par, ap, auc, 4, rslts, R)


        print("Results for nnn.nnn, ltc.nnn, nnn.ltc, ltc.ltc, and random")
        
        print("Precision @ 10\tPrecision @ R\tAverage Precision\tArea Under Curve")
        for i in range(5):
            pa10[i] = pa10[i]/numqueries
            print(pa10[i], end="\t")
            par[i] = par[i]/numqueries
            print(par[i], end="\t")
            ap[i] = ap[i]/numqueries
            print(ap[i], end="\t")
            auc[i] = auc[i]/numqueries
            print(auc[i])

        
        


#Jen
def randomResult(totalURLs, R):
    """
    Returns a boolean true value list that represents a random result.
    """

    booleanRanRslts = []

    for r in range (0,totalURLs-R):
        booleanRanRslts.append(False)

    for r in range (0,R):
        booleanRanRslts.append(True)

    random.shuffle(booleanRanRslts)

    return booleanRanRslts
    
        
    


#Jen
def precisionAt(rslts, R):
    """
    Finds precision at int R (R is the number of relevant results available)
    (number of relevant webpages found in first R results/R)
    """
    if R == 0:
        return 0
    tp = 0
    par = 0
    for i in range(R):
        if rslts[i]:
            tp += 1
    par = tp/R
    return par

    found = 0

    for x in range(0,R):
        if rslts[x]:
            found += 1

    precAtR = found/R

    return precAtR

#Jen
def averagePrecision(rslts, R):
    """
    Averages precision at each True Positive result
    """
    
    if R == 0:
        return 0
    ap = 0
    tp = 0
    i = 0
    while tp < R:
        if rslts[i]:
            tp += 1
            ap += tp/(i+1)
        i += 1
    return ap/tp
            

#Kelly
def auc(rslts, R):
    """
    At each True Negative, multiply the current True Positive rate
    by 1/(number of irrelevant results)
    number of irrelevant results determined by subtracting R
    from total number of results.
    """
    if R == 0:
        return 0
    tp = 0
    auc = 0
    for r in rslts:
        if r:
            tp += 1/R
        else:
            auc += tp * 1/(len(rslts)-R)
    return auc

#new, just for neatness
def evaluateScores(pa10List, parList, apList, aucList, i, rslts, R):
    pa10List[i] += precisionAt(rslts, 10)
    parList[i] += precisionAt(rslts, R)
    apList[i] += averagePrecision(rslts, R)
    aucList[i] += auc(rslts, R)


def main():
    ee = EvaluationEngine("data/clean/", "data/cache.db", "data/nnnindex.p", "data/ltcindex.p")
    ee.evaluate()

main()
