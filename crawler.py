import webdev
import os
import json

# adds the number of times each page is referenced to queue (additional queue counts the number of webpages) and saves data within paragraph tags to files
def readPage(seed):
    webData = webdev.read_url(seed)
    fileName = os.path.join("data", seed[7:].replace("/", "|").rstrip(".html") + ".json")
    fileContents = {}
    i = 0
    while i < len(webData):
        # finds every paragraph tag and checks the link that those link direct to
        if webData[i:i+2] == "<p":
            # GETS DATA WITH P TAG
            if "fileData" in fileContents:
                fileContents["fileData"].append(webData[webData.find(">", i) + 1:webData.find("</p>", i)].strip().split())
            else:
                fileContents["fileData"] = webData[webData.find(">", i) + 1:webData.find("</p>", i)].strip().split()
            # makes next iteration skips the found data
            i = webData.find("</p>", i) + 4
            continue
        if webData[i:i+9] == "<a href=\"":
            # subpathName = webData[i+11:webData.find("\">", i)].strip(".html")
            href = webData[i+9:webData.find("\">", i)]
            if href.startswith("./"):
                fullpath = seed[:seed.rfind("/") + 1] + webData[i+11:webData.find("\">", i)]
            else:
                fullpath = webData[i+11:webData.find("\">", i)]
            if "referenceLinks" in fileContents:
                fileContents["referenceLinks"].append(fullpath)
            else:
                fileContents["referenceLinks"] = [fullpath]
            if not fullpath in queue:
                queue[fullpath] = 1
                # makes next iteration skip the rest of the anchor tag that has already been found
                i = webData.find("</a>", i) + 4
                readPage(fullpath)
            else:
                queue[fullpath] += 1
            # implementation for counting references
            # else:
            #     queue[subpathName] += 1

        i += 1
    with open(fileName, "w") as fileWrite:
        json.dump(fileContents, fileWrite)

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
    global queue
    queue = {}
    removeSavedData()
    os.makedirs("data")
    queue[seed] = 0
    readPage(seed)
    return(len(queue))

# print(crawl("http://people.scs.carleton.ca/~davidmckenney/fruits/N-0.html"))
print(crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))
