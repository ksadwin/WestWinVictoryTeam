# WestWinVictoryTeam

* A search engine developed by Kelly Sadwin (http://github.com/ksadwin) and Jen Westling (http://github.com/JKWest) for Ithaca College COMP 490: Search Engines and Recommender Systems
* Uses Python 3.4
* Contains a boolean search engine (lab3.py) and a ranked retrieval search engine (lab4.py), plus a program to evaluate the accuracy of the ranked retrieval engine
* Uses code from *CS490SearchAndRecommend* (http://github.com/dturnbull/CS490SearchAndRecommend) for web scraping and indexing (spider.py and lab2.py) with minor edits
* Provided with base SQLite3 file webdb.py by Professor Doug Turnbull (dturnbull-AT-ithaca.edu), but includes edits and additions
* Uses module to return Google search results (google.py) by Mario Vilas (http://github.com/MarioVilas/google/) for the purpose of building a corpus of pages

# How to use

* Use of this program requires a folder of files provided in class (should be in the directory data/item/). From these three .txt files, the lab2.py webcrawler, using spider.py, google.py, and webdb.py, will create a corpus.
* After making the corpus, any of the search engines (lab3.py, lab4.py, lab5.py) are usable.
* The *Boolean Search Engine* (lab3.py) performs five query types: single token, AND, OR, NEAR, and phrasal. The last 4 query types only support 2-word queries.
* The *Ranked Retrieval Engine* (lab4.py) takes queries of any length and returns the top 5 documents and item types based on a ranking system of the user's choice (nnn or ltc) for either documents or queries.
* The *Evaluation Engine* (lab5.py) runs queries for each of the items listed in the initial text files and averages the performance across all items for each weighting system (nnn.nnn, nnn.ltc, ltc.nnn, ltc.ltc, plus randomly returned results) to evaluate the performance of the Ranked Retrieval Engine. Spoiler alert: it's pretty good!

# Some quirks

* The google.py web crawler will make Google suspicious of your browsing habits. We faked a header for a regular browser and there are delays incorporated, but many people on our network had to enter a captcha the next time they used Google. As far as we know, no IP addresses were banned or anything drastic, but you have been warned.
* We have included pickles of our own inverted indices for faster running times. If you build your own database, it will not get along with our pickles. We have shared my database but not the text files (it is over 2000 files) which renders our database useless to you. It was really useful to share with each other, though! Maybe delete them before you run any of the search engines. The constructor automatically builds you your own pickle.
* The query "Pirates of the Caribbean: Dead Man's Chest" crashed multiple groups' search engines, even after stripping punctuation. We just skipped that one. We figured it wasn't that big of a deal.
