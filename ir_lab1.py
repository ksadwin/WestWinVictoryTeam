"""
Kelly Sadwin & Jen Westling
2/3/2014
Lab 1: Text pre-processing
"""

import urllib.request
from bs4 import BeautifulSoup
import nltk
import re
import webdb
import json
import google
import os


class Spider:

    def __init__(self, cache):
        self.title = "Untitled"
        self.text = ""
        self.docType = ""
        self.terms = []
        self.header = ""
        if os.path.exists(cache):
            os.remove(cache)
        self.cache = webdb.WebDB(cache)
        

#downloads html of url, prints title, removes tags, tokenizes, prints no. of tokens
    def parser(self, url):
        try:
            #takes the URL and stuffs it in a variable
            firefox = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            firefox = urllib.request.urlopen(firefox)
            #decodes the url into a string
            htmlstring = firefox.read().decode("utf-8", errors="ignore")
            #takes the messy string and sticks it in a Beautiful Soup object
            soupy = BeautifulSoup(htmlstring)
            #sticks the header of the url into a variable so we can smash it
            self.header = str(firefox.info())

            #remove javascript
            for js in soupy.find_all(re.compile("script")):
                js.decompose()
            #remove style
            for style in soupy.find_all(re.compile("style")):
                style.decompose()


            if (soupy.title != None):
                self.title = soupy.title.string.strip()
            self.text = soupy.get_text().strip()

            tokenizer = nltk.RegexpTokenizer("\w+|!-%|'-,|.-?]")
            self.terms = tokenizer.tokenize(self.text)
            #print("Number of tokens:", len(self.terms))
            return htmlstring
        
        except Exception:
            return None

#turns all terms lowercase, calls getTerms to print no. of terms
    def lower(self):
        for i in range(len(self.terms)):
            self.terms[i] = self.terms[i].lower()
        self.getTerms(" after lowercase")

#uses porter stemmer from nltk, calls getTerms to print no. of terms 
    def stem(self):
        stemmer = nltk.stem.porter.PorterStemmer()
        stemList = []
        for term in self.terms:
            stemList.append(stemmer.stem(term))
        self.terms = stemList
        self.getTerms(" after Porter Stemmer")

#casts list as a set, then a list again in order to remove like terms
#strType allows specification of what actions have been done to terms list
    def getTerms(self, strType = ""):
        self.terms = list(set(self.terms))
        self.terms.sort()
        #print("Number of terms"+strType+":", len(self.terms))

    def fetch(self, url):
        #gets text and tokens, ***still need header and database inclusion
        html = self.parser(url)
        if (html != None):
            #put url in database and save the urlID for naming purposes
            title = re.sub(r"['\"]", "", self.title)
            print(title)
            try:
                urlID = self.cache.insertCachedURL(html, self.docType, title)
                filename = (str)(urlID) + ".txt"
                rawfile = open("data/raw/"+filename, "w")
                html = list(html)
                for c in html:
                    try:
                        rawfile.write(c)
                    except UnicodeEncodeError:
                        pass
                
                rawfile.close()

                headerfile = open("data/header/"+filename, "w")
                headerfile.write(self.header)
                headerfile.close()
                
                cleanfile = open("data/clean/"+filename, "w")
                for token in self.terms:
                    try:
                        cleanfile.write(token+"\n")
                    except UnicodeEncodeError:
                        pass
                cleanfile.close()
            except Exception:
                pass

    def search(self, item, itemType):
        query = "\""+item+"\" "+itemType
        print(query)
        results = google.search(query)
        for url in results:
            self.fetch(url)


def main():
    if not os.path.exists("data/"):
        os.path.mkdir("data/")
    if not os.path.exists("data/clean/"):
        os.path.mkdir("data/clean/")
    if not os.path.exists("data/header/"):
        os.path.mkdir("data/header/")
    if not os.path.exists("data/raw/"):
        os.path.mkdir("data/raw/")
    if not os.path.exists("data/item/"):
        os.path.mkdir("data/item/")
        print("hey what u want in ur items thing friend")
        #todo: make that a real thing
    spiderman = Spider("data/cache.db")
    itemList = ["book", "movie", "music"]
    for item in itemList:
        file = open("data/item/"+item+".txt", "r")
        print(item+": ")
        for line in file.readlines():
            spiderman.search(line.strip(), item.strip())
    
    
    

main()
