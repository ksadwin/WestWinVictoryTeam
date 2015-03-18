"""
Lab 5: Evaluation
not sure if this file should have code or just be notes
Let's keep updating this as we find more functions to write!
"""

import os
import webdb

#Kelly
def getQueries():
    """
    This function will use the txt files in the item folder
    to generate the test queries and return them (as a list?)
    so that they can be run as nnn.nnn, nnn.ltc, ltc.nnn, ltc.ltc
    """
    #create list of queries
    queries = []
    #for each of the three item types
    path = "data/item/"
    types = os.listdir(path)
    for t in types:
        f = open(path+t, "r")
        #for each item in the file
        for line in f.readlines():
            line = line.strip("\n")
            #append item+type string to queries list
            queries.append(line+" "+t.strip(".txt"))

    return queries
    

#Jen
def randomResult():
    """
    Returns all webpages in a random order.
    """

#Kelly
def translateResults(item, results):
    """
    Finds number of relevant webpages for a given item.
    Also processes results into true/false list?
    Only processes results into true/false list?
    we shall see
    """
    booleanRslts = []
    R = 0
    #results is a list of docIDs
    for docID in results:
        itemID = webdb.lookupItemIDFromDocID(docID)
        if webdb.lookupItemName(itemID) == item:
            booleanRslts.append(True)
            R += 1
        else:
            booleanRslts.append(False)
    return booleanRslts, R
    
        
    
#Jen
def precisionAt(R):
    """
    Finds precision at int R
    (number of relevant webpages found in first R results/R)
    """

#Jen
def averagePrecision():
    """
    Averages precision at each True Positive result
    """

#Kelly
def auc(rrtuple):
    """
    At each True Negative, multiply the current True Positive rate
    by 1/(number of irrelevant results)
    number of irrelevant results could be determined by subtracting
    R from total number of results.
    """
    rslts = rrtuple[0]
    R = rrtuple[1]
    tp = 0
    auc = 0
    for r in rslts:
        if r:
            tp += 1/R
        else:
            auc += tp * 1/(len(rslts)-R)
    return auc


def main():
    #for testing functions
    #in case that's a thing you want to do
    #(I haven't wanted to do it yet)
