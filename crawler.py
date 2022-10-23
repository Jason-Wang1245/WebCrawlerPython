import webdev
import os
import json
import math
import matmult

# reads all text and link reference data from the given seed
def readPage(seed):
    webData = webdev.read_url(seed)
    fileContents = {"tf": {}, "numWords": {}, "data": {}, "referenceLinks": {}}
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
            fileContents["numWords"] += len(words)
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
            fileContents["referenceLinks"].append(fullpath)
            # ensures that recursion only visits each unique website once
            if not fullpath in checkedPages:
                global index
                index += 1
                checkedPages[fullpath] = index
                # makes next iteration skip the rest of the anchor tag that has already been found
                i = webData.find("</a>", i) + 4
                readPage(fullpath)

        i += 1
    # adds tf values to the fileContents
    for word in fileContents["data"]:
        # add the number of times each word appears in each webpage
        if word in wordCounter:
            wordCounter[word] += 1
        else:
            wordCounter[word] = 1
        # calculates tf score for each word within the current seed (webpage)
        fileContents["tf"][word] = fileContents["data"][word] / fileContents["numWords"]
    # removes data on all words within the current page as it is not needed
    del fileContents["data"]

    fileWrite = open(os.path.join("pageData", seed[7:].replace("/", "}") + ".json"), "w")
    json.dump(fileContents, fileWrite)
    fileWrite.close()

# clears all local cache files and folders
def removeSavedData():
    if os.path.exists("pageData"):
        dataFiles = os.listdir("pageData")
        for file in dataFiles:
            os.remove(os.path.join("pageData", file))
        os.rmdir("pageData")
    if os.path.exists("idf"):
        dataFiles = os.listdir("idf")
        for file in dataFiles:
            os.remove(os.path.join("idf", file))
        os.rmdir("idf")

# saves idf values within a json file
def saveIdf():
    for word in wordCounter:
        idf[word] = math.log(len(checkedPages) / (1 + wordCounter[word]), 2)
    fileWrite = open(os.path.join("idf", "idf.json"), "w")
    json.dump(idf, fileWrite)
    fileWrite.close()

# calculates the page rank of each page and saves it to global variable pageRank
def calculatePageRank():
    pageFiles = os.listdir("pageData")
    vectorA = [[1/len(checkedPages)] * len(checkedPages)]
    euclideanDistance = 1
    # let N represent the number of webpages
    # creates a matrix that has N indices
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
    
    # saves calculated page rank values to a pageRank
    for file in pageFiles:
        pageRank[file] = vectorB[0][checkedPages["http://" + file.replace("}", "/").strip(".json")]]

# writes all the additional values to each individual webpages json cache file
def writeAdditionalData():
    pageFiles = os.listdir("pageData")
    for file in pageFiles:
        # retrieves what is currently written in each page file
        fileRead = open(os.path.join("pageData", file), "r")
        fileData = json.load(fileRead)
        fileRead.close()
        # calculate tf-idf for current page and add it to the current page json data
        fileData["tf-idf"] = {}
        for word in fileData["tf"]:
            fileData["tf-idf"][word] = math.log(1 + fileData["tf"][word], 2) * idf[word]
        # adds page rank and outgoing links to the current page json data
        fileData["pageRank"] = pageRank[file]
        fileData["outgoingLinks"] = outgoingLinks["http://" + file.replace("}", "/").strip(".json")]
        fileWrite = open(os.path.join("pageData", file), "w")
        json.dump(fileData, fileWrite)
        fileWrite.close()
    

# crawls all webpages within in the given seed page and store data in json files
def crawl(seed):
    if webdev.read_url(seed) == "":
        return None
    # keeps track of all check webpapages and index for calculating page rank
    global checkedPages
    checkedPages = {seed: 0}
    # stores all outgoing links
    global outgoingLinks
    outgoingLinks = {}
    # stores the appearence of each word in all pages
    global wordCounter
    wordCounter = {}
    # index used for checkedPages (required for calculating page rank)
    global index
    index = 0
    # stores idf values
    global idf
    idf = {}
    # stores page rank values
    global pageRank
    pageRank = {}
    # clears cache directories and makes new ones
    removeSavedData()
    os.makedirs("pageData")
    os.makedirs("idf")
    # calls readPage to crawl webpages
    readPage(seed)
    # saves additional values of data
    saveIdf()
    calculatePageRank()
    writeAdditionalData()
    return(len(checkedPages))