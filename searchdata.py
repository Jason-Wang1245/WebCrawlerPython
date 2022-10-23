import os
import json
import webdev
import math

def get_incoming_links(URL):
    folderPath = os.path.join("pageData", URL[7:].replace("/", "}"))
    if not os.path.isdir(folderPath):
        return None
    fileRead = open(os.path.join(folderPath, "referenceLinks.json"), "r")
    referenceLinks = json.load(fileRead)["referenceLinks"]
    fileRead.close()
    return referenceLinks

def get_outgoing_links(URL):
    folderPath = os.path.join("pageData", URL[7:].replace("/", "}"))
    if not os.path.isdir(folderPath):
        return None
    fileRead = open(os.path.join(folderPath, "outgoingLinks.json"))
    outgoingLinks = json.load(fileRead)["outgoingLinks"]
    fileRead.close()
    return outgoingLinks

def get_tf(URL, word):
    folderPath = os.path.join("pageData", URL[7:].replace("/", "}"))
    if not os.path.isdir(folderPath):
        return 0
    fileRead = open(os.path.join(folderPath, "tf.json"), "r")
    tf = json.load(fileRead)
    fileRead.close()
    if not word.lower() in tf:
        return 0
    return tf[word.lower()]

def get_idf(word):
    fileRead = open(os.path.join("idf", "idf.json"), "r")
    idf = json.load(fileRead)
    fileRead.close()
    if not word.lower() in idf:
        return 0

    return idf[word.lower()]

def get_tf_idf(URL, word):
    folderPath = os.path.join("pageData", URL[7:].replace("/", "}"))
    if not os.path.isdir(folderPath):
        return 0
    fileRead = open(os.path.join(folderPath, "tf-idf.json"), "r")
    tfIdf = json.load(fileRead)
    if not word.lower() in tfIdf:
        return 0
    return tfIdf[word.lower()]

def get_page_rank(URL):
    folderPath = os.path.join("pageData", URL[7:].replace("/", "}"))
    if not os.path.isdir(folderPath):
        return -1
    fileRead = open(os.path.join(folderPath, "pageRank.txt"), "r")
    pageRank = float(fileRead.read())
    fileRead.close()
    return pageRank

# gets the title of the given webpage (used in search.py)
def get_title(URL):
    folderPath = os.path.join("pageData", URL[7:].replace("/", "}"))
    if not os.path.isdir(folderPath):
        return 0
    fileRead = open(os.path.join(folderPath, "title.txt"), "r")
    title = fileRead.read().strip()
    fileRead.close()
    return title