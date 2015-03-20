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
def randomResult():
    """
    Returns all webpages in a random order.
    """

#Kelly
#translateResults() has been moved to query.py
#because it requires use of the database
    
        
    
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
