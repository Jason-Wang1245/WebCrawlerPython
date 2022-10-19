import webdev
import os
import json
import math

# reads all text and link reference data from the given webpage
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

# multiples matrix with a scalar
def multScalar(matrix, scale):
    # multiplies each individual element within matrix by scale
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] *= scale
    return matrix

# multiples two matrices
def multMatrix(a, b):
    # returns None if the two matrices are incompatible for multiplication
    if len(a[0]) != len(b):
        return None
    # transposes matrix b (swaps rows with columns)
    bChanged = []
    for i in range(len(b[0])):
        bChanged.append([])
        for k in range(len(b)):
            bChanged[i].append(b[k][i])

    matrix = []
    for i in range(len(a)):
        # adds a new row to the product matrix
        matrix.append([])
        # multiples the first row elements of matrix a with the corresponding element in each row of matrix bChanged
        for j in range(len(bChanged)):
            # reset sum for each row in bChanged
            sum = 0
            for k in range(len(bChanged[0])):
                sum += a[i][k] * bChanged[j][k]
            # adds the product sum of each row in matrix bChanged as a new element in the product matrix (in row i)
            matrix[i].append(sum)

    return matrix

# gets euclidian distance between two vectors
def euclideanDist(a, b):
    sum = 0
    # gets the difference of each element in matrix a and b and square it, then add it to sum
    for i in range(len(a[0])):
        sum += (a[0][i] - b[0][i]) ** 2
    # returns the square root of sum (euclidean distance)
    return sum ** (1 / 2)

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
    adjacencyMatrix = multScalar(adjcencyMatrix, 1 - 0.1)
    # adds alpha(0.1)/N
    for i in range(len(checkedPages)):
        for j in range(len(checkedPages)):
            adjacencyMatrix[i][j] += 0.1 / len(checkedPages)

    # keeps getting multiplying the two matrices until their euclidean distance is less than or equal to 0.0001
    vectorB = vectorA
    while euclideanDistance > 0.0001:
        vectorA = vectorB
        vectorB = multMatrix(vectorA, adjacencyMatrix)
        euclideanDistance = euclideanDist(vectorA, vectorB)
    
    # saves calculated page rank values to a json file
    pageRank = {}
    for file in pageFiles:
        name = "http://" + file.replace("}", "/").strip(".json")
        pageRank[name] = vectorB[0][checkedPages[name]]

    fileWrite = open(os.path.join("otherData", "pageRank.json"), "w")
    json.dump(pageRank, fileWrite)
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
    idf = {}
    for word in wordCounter:
        idf[word] = math.log(len(checkedPages) / (1 + wordCounter[word]), 2)
    fileWrite = open(os.path.join("otherData", "idf.json"), "w")
    json.dump(idf, fileWrite)
    fileWrite.close()
    savePageRank()
    return(len(checkedPages))

# print(crawl("http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html"))
# crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")