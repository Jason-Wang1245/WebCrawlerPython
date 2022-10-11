import webdev
import os

# creates a queue of all the files that need to be crawled


def createQueue(seed):
    webData = webdev.read_url(seed)
    path = os.path.join(
        "data", seed[seed.rfind("/") + 1:].strip(".html") + ".txt")
    fileContents = ""
    i = 0
    while i < len(webData):
        # finds every anchor tag and checks the link that those link direct to
        if webData[i:i+3] == "<p>":
            # GETS DATA WITH P TAG
            fileContents += webData[i+3:webData.find("</p>", i)].strip() + "\n"
            # makes so next iteration skips the found data
            i = webData.find("</p>", i) + 4
            continue
        if webData[i:i+9] == "<a href=\"":
            # subpathName = webData[i+11:webData.find("\">", i)].strip(".html")
            fullpath = seed[:seed.rfind("/") + 1] + \
                webData[i+11:webData.find("\">", i)]
            if not fullpath in queue:
                queue[fullpath] = 1
                createQueue(fullpath)
            else:
                queue[fullpath] += 1
            # implementation for counting references
            # else:
            #     queue[subpathName] += 1

        i += 1
    fileWrite = open(path, "w")
    fileWrite.write(fileContents)
    fileWrite.close()


def removeSavedData():
    if os.path.exists("data"):
        dataFiles = os.listdir("data")
        for file in dataFiles:
            os.remove(os.path.join("data", file))
        os.rmdir("data")


def crawl(seed):
    global queue
    queue = {}
    removeSavedData()
    os.makedirs("data")
    # seed[seed.rfind("/") + 1:].strip(".html")
    queue[seed] = 0
    createQueue(seed)
    # while i < len(data):
    #     if data[i] == "<":
    #         if data[i:i+3] == "<p>":
    #             # GETS DATA WITH P TAG
    #             # data[i+3:data.find("</p>", i)].strip()
    #             # makes so next iteration skips the found data
    #             i = data.find("</p>", i) + 4
    #             continue
    #         if data[i:i+9] == "<a href=\"":
    #             subpathName = data[i+11:data.find("\">", i)].strip(".html")
    #             if not subpathName in queue:
    #                 queue[subpathName] = seed[:seed.rfind(
    #                     "/") + 1] + data[i+11:data.find("\">", i)]
    # i += 1
    print(queue)


crawl("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html")
# removeSavedData()


# CODE PORTIONS FOR LATER
# Creates directory storing the data file
# os.makedirs("data")
# fileName = seed[seed.rfind("/") + 1:].strip(".html") + ".txt"
# filePath = os.path.join("data", fileName)
# fileWrite = open(filePath, "w")
# fileWrite.write("hello")
# fileWrite.close()
# Deletes all data files
# files = os.listdir("data")
# for file in files:
#     os.remove(os.path.join("data", file))
# os.rmdir("data")
