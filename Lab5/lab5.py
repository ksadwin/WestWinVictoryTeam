"""
Lab 5: Evaluation
not sure if this file should have code or just be notes
Let's keep updating this as we find more functions to write!
"""

import os
from Lab5 import webdb
import random

#Kelly
def getQueries():
    """
    This function will use the txt files in the item folder
    to generate the test queries and return them (as a list)
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
            queries.append(line)

    return queries
    

#Jen
def randomResult(totalURLS):
    """
    Returns a boolean true value list that represents a random result.
    12 books, 14 movies, 13 musical artist = 39 items.
    763/39 is about 20 so it adds 20 true results to the list and randomizes it.
    """

    booleanRanRslts = []

    for r in range (0,743):
        booleanRanRslts.append(False)

    for r in range (0,20):
        booleanRanRslts.append(True)

    booleanRanRslts = random.shuffle(booleanRanRslts)

    print (booleanRanRslts)

    return booleanRanRslts


#Kelly
#translateResults() has been moved to query.py
#because it requires use of the database
    
        
#Jen
def precisionAt10(rslts, R):
    """
    Finds precision in the top 10 results out of R (R is the number of relevant results available)
    (number of relevant webpages found in first 10 results/R)
    """

    found = 0

    for x in range(0,10):
        if rslts[x]:
            found += 1

    precAt10 = found/R

    return precAt10

#Jen
def precisionAt(rslts, R):
    """
    Finds precision at int R (R is the number of relevant results available)
    (number of relevant webpages found in first R results/R)
    """

    found = 0

    for x in range(0,R):
        if rslts[x]:
            found += 1

    precAtR = found/R

    return precAtR

#Jen
def averagePrecision(rslts, R):
    """
    Averages precision at each True Positive result.
    """
    found = 0
    totalPrecAtR = 0.0

    for x in range (0,R):
        if rslts[x]:
            found += 1
            totalPrecAtR += (found/x)

    avgPrec = (totalPrecAtR/found)

    return avgPrec

#Kelly
def auc(rslts, R):
    """
    At each True Negative, multiply the current True Positive rate
    by 1/(number of irrelevant results)
    number of irrelevant results determined by subtracting R
    from total number of results.
    """
    tp = 0
    auc = 0
    for r in rslts:
        if r:
            tp += 1/R
        else:
            auc += tp * 1/(len(rslts)-R)
    return auc

"""
def main():
    #for testing functions
    
    
main()
"""
