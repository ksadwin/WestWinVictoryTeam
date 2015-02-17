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
#import webdb
import os, sys
#import spider


def main():
    #find the cache?
    
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
            print("single token")
        elif search == "2":
            print("AND")
        elif search == "3":
            print("OR")
        elif search == "4":
            print("phrase")
        elif search == "5":
            print("NEAR")
        elif search != "0":
            print("Invalid input.")
    print("Goodbye")

main()
