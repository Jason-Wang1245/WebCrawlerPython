import os
import json
import webdev
import math

def get_incoming_links(URL):
    filePath = os.path.join("data", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return None

    fileRead = open(filePath, "r")
    fileContents = json.load(fileRead)
    fileRead.close()
    return fileContents["referenceLinks"]

def get_outgoing_links(URL):
    if not os.path.isfile(os.path.join("data", URL[7:].replace("/", "}") + ".json")):
        return None
    links = []
    files = os.listdir("data")
    for file in files:
        filePath = os.path.join("data", file)
        with open(filePath, "r") as fileRead:
            fileContents = json.load(fileRead)
        for link in fileContents["referenceLinks"]:
            if link == URL:
                links.append("https://" + file.replace("}", "/")[:len(file) - 5] + ".html")
    return links

# def get_page_rank(URL):

def get_tf(URL, word):
    filePath = os.path.join("data", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return 0
    
    fileRead = open(filePath, "r")
    fileData = json.load(fileRead)
    fileRead.close()
    if not word.lower() in fileData["data"]:
        return 0

    return fileData["data"][word.lower()] / fileData["numWords"]

def get_idf(word):
    numWordAppearence = 0
    files = os.listdir("data")
    for file in files:
        filePath = os.path.join("data", file)
        fileRead = open(filePath, "r")
        fileData = json.load(fileRead)["data"]
        fileRead.close()
        if word.lower() in fileData:
            numWordAppearence += 1
    return math.log(len(files) / (1 + numWordAppearence), 2)

def get_tf_idf(URL, word):
    return math.log(1 + get_tf(URL, word), 2) * get_idf(word)

print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html", "apple"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html", "apple"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-2.html", "apple"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-3.html", "apple"))

print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html", "banana"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html", "Banana"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-2.html", "BANANA"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-3.html", "banana"))

print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html", "peach"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-1.html", "peach"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-2.html", "peach"))
print(get_tf_idf("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-3.html", "peach"))