import webdev
import os
import json
import math
import matmult

# reads all text and link reference data from the given webpage
def readPage(seed):
    webData = webdev.read_url(seed)
    fileContents = {"tf": {}}
    i = 0
    while i < len(webData):
        # gets the title of the page
        if webData[i:i+7] == "<title>":
            fileContents["title"] = webData[i+7:webData.find("</title>")]
            i = webData.find("</title>") + 8
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
            if not fullpath in checkedPages:
                global index
                index += 1
                checkedPages[fullpath] = index
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

    del fileContents["data"]

    fileWrite = open(os.path.join("pageData", seed[7:].replace("/", "}") + ".json"), "w")
    json.dump(fileContents, fileWrite)
    fileWrite.close()

# clears all local data files
def removeSavedData():
    if os.path.exists("pageData"):
        dataFiles = os.listdir("pageData")
        for file in dataFiles:
            os.remove(os.path.join("pageData", file))
        os.rmdir("pageData")
    if os.path.exists("otherData"):
        dataFiles = os.listdir("otherData")
        for file in dataFiles:
            os.remove(os.path.join("otherData", file))
        os.rmdir("otherData")

def savePageRank():
    pageFiles = os.listdir("pageData")
    vectorA = [[0] * len(checkedPages)]
    vectorA[0][0] = 1
    euclideanDistance = 1
    # let N represent the number of webpages
    # creates a matrix that has N indexes
    adjcencyMatrix = [0] * len(checkedPages)
    # adds 1 to each index where a page references another
    for file in pageFiles:
        name = "http://" + file.replace("}", "/").strip(".json")
        fileRead = open(os.path.join("pageData", file))
        referenceLinks = json.load(fileRead)["referenceLinks"]
        row = [0] * len(checkedPages)
        for link in referenceLinks:
            # adds 1 to each index that represents an outgoing reference
            row[checkedPages[link]] = 1 / len(referenceLinks)
        # adds the row into the corresponding index of the current page (name)
        adjcencyMatrix[checkedPages[name]] = row

    # multiples entire matrix by 1 - alpha(0.1)
    adjacencyMatrix = matmult.mult_scalar(adjcencyMatrix, 1 - 0.1)
    # adds alpha(0.1)/N
    for i in range(len(checkedPages)):
        for j in range(len(checkedPages)):
            adjacencyMatrix[i][j] += 0.1 / len(checkedPages)

    # keeps getting multiplying the two matrices until their euclidean distance is less than or equal to 0.0001
    vectorB = vectorA
    while euclideanDistance > 0.0001:
        vectorA = vectorB
        vectorB = matmult.mult_matrix(vectorA, adjacencyMatrix)
        euclideanDistance = matmult.euclidean_dist(vectorA, vectorB)
    
    # saves calculated page rank values to a json file
    pageRank = {}
    for file in pageFiles:
        name = "http://" + file.replace("}", "/").strip(".json")
        pageRank[name] = vectorB[0][checkedPages[name]]

    fileWrite = open(os.path.join("otherData", "pageRank.json"), "w")
    json.dump(pageRank, fileWrite)
    fileWrite.close()

def saveTfIdf():
    pageFiles = os.listdir("pageData")
    for file in pageFiles:
        fileRead = open(os.path.join("pageData", file), "r")
        fileData = json.load(fileRead)
        fileRead.close()
        fileData["tf-idf"] = {}
        for word in fileData["tf"]:
            fileData["tf-idf"][word] = math.log(1 + fileData["tf"][word], 2) * idf[word]
        fileWrite = open(os.path.join("pageData", file), "w")
        json.dump(fileData, fileWrite)
        fileWrite.close()
    

# crawls all webpages within in the given seed page and store data in json files
def crawl(seed):
    if webdev.read_url(seed) == "":
        return None
    # creates global dictionaries used for readPage
    # used to give each webpage a unique index
    global checkedPages
    checkedPages = {seed: 0}
    global outgoingLinks
    outgoingLinks = {}
    global wordCounter
    wordCounter = {}
    global index
    index = 0
    # clears cache directories and makes new ones
    removeSavedData()
    os.makedirs("pageData")
    os.makedirs("otherData")
    # calls readPage to crawl webpages
    readPage(seed)
    # create file for outgoing links in data directory
    fileWrite = open(os.path.join("otherData", "outgoingLinks.json"), "w")
    json.dump(outgoingLinks, fileWrite)
    fileWrite.close()
    # calculate all idf values and create file for storing them in data directory
    global idf
    idf = {}
    for word in wordCounter:
        idf[word] = math.log(len(checkedPages) / (1 + wordCounter[word]), 2)
    fileWrite = open(os.path.join("otherData", "idf.json"), "w")
    json.dump(idf, fileWrite)
    fileWrite.close()
    savePageRank()
    saveTfIdf()
    return(len(checkedPages))