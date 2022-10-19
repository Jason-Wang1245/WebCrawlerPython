import webdev
import os
import json
import math
import time

# adds the number of times each page is referenced to queue (additional queue counts the number of webpages) and saves data within paragraph tags to files
def readPage(seed):
    webData = webdev.read_url(seed)
    fileContents = {"tf": {}}
    i = 0
    while i < len(webData):
        # finds every paragraph tag and checks the link that those link direct to
        if webData[i:i+2] == "<p":
            if not "data" in fileContents:
                fileContents["data"] = {}
            words = webData[webData.find(">", i) + 1:webData.find("</p>", i)].strip().split()
            # adds all words within the paragraph tag to fileContents
            for word in words:
                word = word.lower()

                if word in fileContents["data"]:
                    fileContents["data"][word] += 1
                else:
                    fileContents["data"][word] = 1
            # adds the total of words just added to fileContents
            if "numWords" in fileContents:
                fileContents["numWords"] += len(words)
            else:
                fileContents["numWords"] = len(words)
            # makes next iteration skips the found data
            i = webData.find("</p>", i) + 4
            continue
        if webData[i:i+2] == "<a":
            href = webData[webData.find("href=\"", i) + 6:webData.find("\">", i)]
            # checks if the anchor tag is a relative link
            if href.startswith("./"):
                fullpath = seed[:seed.rfind("/") + 1] + href[2:]
            else:
                fullpath = href
            # adds outgoing links to outgoingLinks, which will be stored as a file later
            if fullpath in outgoingLinks:
                outgoingLinks[fullpath].append(seed)
            else:
                outgoingLinks[fullpath] = [seed]
            # add reference link to fileContents
            if "referenceLinks" in fileContents:
                fileContents["referenceLinks"].append(fullpath)
            else:
                fileContents["referenceLinks"] = [fullpath]
            # ensures that recursion only visits each unique website once
            if not fullpath in queue:
                queue[fullpath] = 0
                # makes next iteration skip the rest of the anchor tag that has already been found
                i = webData.find("</a>", i) + 4
                readPage(fullpath)

        i += 1
    for word in fileContents["data"]:
        # add the number of times each word appears in each webpage
        if word in wordCounter:
            wordCounter[word] += 1
        else:
            wordCounter[word] = 1
        # calculates tf score for each word within the current seed (webpage)
        fileContents["tf"][word] = fileContents["data"][word] / fileContents["numWords"]

    fileWrite = open(os.path.join("data", seed[7:].replace("/", "}") + ".json"), "w")
    json.dump(fileContents, fileWrite)
    fileWrite.close()

# clears all local data files
def removeSavedData():
    if os.path.exists("data"):
        dataFiles = os.listdir("data")
        for file in dataFiles:
            os.remove(os.path.join("data", file))
        os.rmdir("data")

# crawls all webpages within in the given seed page and store data in json files
def crawl(seed):
    if webdev.read_url(seed) == "":
        return None
    # creates global dictionaries used later
    global queue
    queue = {seed: 0}
    global outgoingLinks
    outgoingLinks = {}
    global wordCounter
    wordCounter = {}
    # clears cache
    removeSavedData()
    os.makedirs("data")
    # calls readPage to crawl webpages
    readPage(seed)
    # create file for outgoing links in data directory
    fileWrite = open(os.path.join("data", "outgoingLinks.json"), "w")
    json.dump(outgoingLinks, fileWrite)
    fileWrite.close()
    # calculate all idf values and create file for storing them in data directory
    idf = {}
    for word in wordCounter:
        idf[word] = math.log(len(queue) / (1 + wordCounter[word]), 2)
    fileWrite = open(os.path.join("data", "idf.json"), "w")
    json.dump(idf, fileWrite)
    fileWrite.close()
    return(len(queue))

# start = time.time()
# print(crawl("http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html"))
# print(time.time() - start)
print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))