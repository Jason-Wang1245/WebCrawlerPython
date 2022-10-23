import os
import json
import webdev
import math

def get_incoming_links(URL):
    filePath = os.path.join("pageData", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return None

    fileRead = open(filePath, "r")
    referenceLinks = json.load(fileRead)["referenceLinks"]
    fileRead.close()
    return referenceLinks

def get_outgoing_links(URL):
    filePath = os.path.join("pageData", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return None
    
    fileRead = open(filePath, "r")
    outgoingLinks = json.load(fileRead)["outgoingLinks"]
    fileRead.close()
    return outgoingLinks

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
    fileRead = open(os.path.join("idf", "idf.json"), "r")
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
    
    fileRead = open(filePath, "r")
    pageRank = json.load(fileRead)["pageRank"]
    fileRead.close()
    return pageRank

# gets the title of the given webpage (used in search.py)
def get_title(URL):
    filePath = os.path.join("pageData", URL[7:].replace("/", "}") + ".json")
    if not os.path.isfile(filePath):
        return None
    
    fileRead = open(filePath, "r")
    pageTitle = json.load(fileRead)["title"]
    fileRead.close()
    return pageTitle