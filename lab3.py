"""
Lab 3: Boolean Retrieval
Kelly Sadwin & Jen Westling
The BooleanSearchEngine (inherits SearchEngine) supports 5 query types:
1. single token
2. AND query
3. OR query
4. 2-token phrasal query
5. NEAR query
using a positional index
"""

from query import SearchEngine

class BooleanSearchEngine(SearchEngine):

    def __init__(self, dirLocation, cache, indexp):
        SearchEngine.__init__(self, dirLocation, cache, indexp)


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


    def menu(self):
        
        search = ""
        while search != "0":
            print(" 1. single token query")
            print(" 2. AND query")
            print(" 3. OR query")
            print(" 4. phrase query")
            print(" 5. NEAR query")
            search = input("Enter number for search type, or 0 to quit: ")
            if search == "1":
                self.singleToken()
            elif search == "2":
                self.booleanAND()
            elif search == "3":
                self.booleanOR()
            elif search == "4":
                self.phraseQuery()
            elif search == "5":
                self.nearQuery()
            elif search != "0":
                print("Invalid input.")
        print("Goodbye")


def main():
    bse = BooleanSearchEngine("data/clean/", "data/cache.db", "data/nnnindex.p")
    bse.menu()

main()
