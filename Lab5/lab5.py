"""
Lab 5: Evaluation
not sure if this file should have code or just be notes
Let's keep updating this as we find more functions to write!
"""

#Kelly
def runQueries():
    """
    This function will use the txt files in the item folder
    to generate the test queries and return them (as a list?)
    so that they can be run as nnn.nnn, nnn.ltc, ltc.nnn, ltc.ltc
    """

#Jen
def randomResult():
    """
    Returns all webpages in a random order.
    """

#Kelly
def getR(item):
    """
    Finds number of relevant webpages for a given item.
    """
    
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
def auc():
    """
    At each True Negative, multiply the current True Positive rate
    by 1/(number of irrelevant results)
    number of irrelevant results could be determined by subtracting
    R from total number of results.
    """
