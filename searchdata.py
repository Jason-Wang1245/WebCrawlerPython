import os
import json
import webdev
import math

def get_incoming_links(URL):
    filePath = os.path.join("pageData", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return None

    fileRead = open(filePath, "r")
    fileContents = json.load(fileRead)
    fileRead.close()
    return fileContents["referenceLinks"]

def get_outgoing_links(URL):
    if not os.path.isfile(os.path.join("pageData", URL[7:].replace("/", "}") + ".json")):
        return None
    
    fileRead = open(os.path.join("otherData", "outgoingLinks.json"), "r")
    outgoingLinks = json.load(fileRead)
    fileRead.close()
    return outgoingLinks[URL]

def get_tf(URL, word):
    filePath = os.path.join("pageData", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return 0
    
    fileRead = open(filePath, "r")
    tfValues = json.load(fileRead)["tf"]
    fileRead.close()
    if not word.lower() in tfValues:
        return 0

    return tfValues[word.lower()]

def get_idf(word):
    fileRead = open(os.path.join("otherData", "idf.json"), "r")
    idfValues = json.load(fileRead)
    fileRead.close()
    if not word.lower() in idfValues:
        return 0

    return idfValues[word.lower()]

def get_tf_idf(URL, word):
    filePath = os.path.join("pageData", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return 0

    fileRead = open(filePath, "r")
    tfIdf = json.load(fileRead)["tf-idf"]
    if word.lower() in tfIdf:
        return tfIdf[word.lower()]
    else:
        return 0

def get_page_rank(URL):
    filePath = os.path.join("pageData", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return -1
    
    fileRead = open(os.path.join("otherData", "pageRank.json"))
    pageRank = json.load(fileRead)[URL]
    fileRead.close()
    return pageRank

def get_title(URL):
    filePath = os.path.join("pageData", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return None
    
    fileRead = open(filePath, "r")
    pageTitle = json.load(fileRead)["title"]
    fileRead.close()
    return pageTitle