import webdev
import os
import json
import math
import matmult

# reads all text and link reference data from the given seed
def readPage(seed):
    webData = webdev.read_url(seed)
    folderPath = os.path.join("pageData", seed[7:].replace("/", "}"))
    os.makedirs(folderPath)
    # local variables that stores data later to be written to files
    data = {}
    tf = {}
    referenceLinks = {"referenceLinks": []}
    numWords = 0
    i = 0
    # iterates through html code of the given seed
    while i < len(webData):
        # gets the title of the page
        if webData[i:i+7] == "<title>":
            title = webData[i+7:webData.find("</title>")]
            i = webData.find("</title>") + 8
        # finds every paragraph tag
        if webData[i:i+2] == "<p":
            words = webData[webData.find(">", i) + 1:webData.find("</p>", i)].strip().split()
            # add all words within the paragraph tag to data (counter system using dictionary)
            for word in words:
                word = word.lower()
                if word in data:
                    data[word] += 1
                else:
                    data[word] = 1
            # adds the total number of words just found within the paragraph tag to numWords
            numWords += len(words)
            # makes next iteration skip the found data
            i = webData.find("</p>", i) + 4
            continue
        # finds every anchor tag
        if webData[i:i+2] == "<a":
            href = webData[webData.find("href=\"", i) + 6:webData.find("\">", i)]
            # checks if the anchor tag is a relative link
            if href.startswith("./"):
                fullpath = seed[:seed.rfind("/") + 1] + href[2:]
            else:
                fullpath = href
            # adds outgoing links to the according page in outgoingLinks, which will be stored as a file later
            if fullpath in outgoingLinks:
                outgoingLinks[fullpath].append(seed)
            else:
                outgoingLinks[fullpath] = [seed]
            # adds link to referenceLinks
            referenceLinks["referenceLinks"].append(fullpath)
            # ensures that recursion only visits each unique website once
            if not fullpath in checkedPages:
                # index used to identify elements within adjacency matrix when calculating page rank
                global index
                index += 1
                checkedPages[fullpath] = index
                # makes next iteration skip the rest of the anchor tag that has already been found
                i = webData.find("</a>", i) + 4
                readPage(fullpath)
        i += 1

    # adds tf values to the variable tf
    for word in data:
        # add the number of times each word appears in each webpage (later used to calculate idf)
        if word in wordCounter:
            wordCounter[word] += 1
        else:
            wordCounter[word] = 1
        # calculates tf score for each word within the current seed (webpage)
        tf[word] = data[word] / numWords

    # seperates each calculated data seciton to their according file within the webpage folder
    fileWrite = open(os.path.join(folderPath, "tf.json"), "w")
    json.dump(tf, fileWrite)
    fileWrite = open(os.path.join(folderPath, "referenceLinks.json"), "w")
    json.dump({"referenceLinks": referenceLinks["referenceLinks"]}, fileWrite)
    fileWrite = open(os.path.join(folderPath, "title.txt"), "w")
    fileWrite.write(title)
    fileWrite.close()


# clears all local cached files and folders
def removeSavedData():
    if os.path.exists("pageData"):
        dataFolders = os.listdir("pageData")
        for folder in dataFolders:
            folderPath = os.path.join("pageData", folder)
            dataFiles = os.listdir(folderPath)
            for file in dataFiles:
                os.remove(os.path.join(folderPath, file))
            os.rmdir(folderPath)
        os.rmdir("pageData")
    if os.path.exists("idf"):
        dataFiles = os.listdir("idf")
        for file in dataFiles:
            os.remove(os.path.join("idf", file))
        os.rmdir("idf")

# calculate and save idf values within a json file
def saveIdf():
    for word in wordCounter:
        idf[word] = math.log(len(checkedPages) / (1 + wordCounter[word]), 2)
    fileWrite = open(os.path.join("idf", "idf.json"), "w")
    json.dump(idf, fileWrite)
    fileWrite.close()

# calculates the page rank of each page and saves it to global variable pageRank
def calculatePageRank():
    pageFolders = os.listdir("pageData")
    # creates the initial vector with sum of all elements adding up to 1 (later used to calculate euclidian distance for page rank score)
    vectorA = [[1/len(checkedPages)] * len(checkedPages)]
    euclideanDistance = 1
    # let N represent the number of webpages
    # creates a matrix that has N indices
    adjcencyMatrix = [0] * len(checkedPages)
    # adds 1 / N to each index where a page references another
    for folder in pageFolders:
        folderPath = os.path.join("pageData", folder)
        name = "http://" + folder.replace("}", "/")
        fileRead = open(os.path.join(folderPath, "referenceLinks.json"), "r")
        referenceLinks = json.load(fileRead)["referenceLinks"]
        # creates the rows for the matrix with length of N
        row = [0] * len(checkedPages)
        for link in referenceLinks:
            row[checkedPages[link]] = 1 / len(referenceLinks)
        # adds the row into the corresponding index of the current page (name)
        adjcencyMatrix[checkedPages[name]] = row

    # multiples entire matrix by 1 - alpha(0.1)
    adjacencyMatrix = matmult.mult_scalar(adjcencyMatrix, 1 - 0.1)
    # adds alpha(0.1)/N to entire matrix
    for i in range(len(checkedPages)):
        for j in range(len(checkedPages)):
            adjacencyMatrix[i][j] += 0.1 / len(checkedPages)

    # keeps getting multiplying the two matrices until their euclidean distance is less than or equal to 0.0001
    vectorB = vectorA
    while euclideanDistance > 0.0001:
        vectorA = vectorB
        vectorB = matmult.mult_matrix(vectorA, adjacencyMatrix)
        euclideanDistance = matmult.euclidean_dist(vectorA, vectorB)
    
    # saves calculated page rank values to pageRank
    for folder in pageFolders:
        pageRank[folder] = vectorB[0][checkedPages["http://" + folder.replace("}", "/").strip(".json")]]

# writes all the additional values to each accoding files within each webpage folder
def writeAdditionalData():
    pageFolders = os.listdir("pageData")
    for folder in pageFolders:
        folderPath = os.path.join("pageData", folder)
        fileRead = open(os.path.join(folderPath, "tf.json"), "r")
        tf = json.load(fileRead)
        fileRead.close()
        # calculate tf-idf for current page and add it to the current page data folder
        tfIdf = {}
        for word in tf:
            tfIdf[word] = math.log(1 + tf[word], 2) * idf[word]
        fileWrite = open(os.path.join(folderPath, "tf-idf.json"), "w")
        json.dump(tfIdf, fileWrite)
        # adds page rank and outgoing links to the current page data folder
        fileWrite = open(os.path.join(folderPath, "pageRank.txt"), "w")
        fileWrite.write(str(pageRank[folder]))
        fileWrite = open(os.path.join(folderPath, "outgoingLinks.json"), "w")
        json.dump({"outgoingLinks": outgoingLinks["http://" + folder.replace("}", "/").strip(".json")]}, fileWrite)
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
    # saves and calcualtes additional values
    saveIdf()
    calculatePageRank()
    writeAdditionalData()
    return(len(checkedPages))