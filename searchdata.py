import os
import json
import webdev

def get_incoming_links(URL):
    filePath = os.path.join("data", URL[7:].replace("/", "|").rstrip(".html") + ".json")
    if not os.path.isfile(filePath):
        return None

    with open(filePath, "r") as fileRead:
        fileContents = json.load(fileRead)
    return fileContents["referenceLinks"]

def get_outgoing_links(URL):
    if not os.path.isfile(os.path.join("data", URL[7:].replace("/", "|").rstrip(".html") + ".json")):
        return None
    links = []
    files = os.listdir("data")
    for file in files:
        filePath = os.path.join("data", file)
        with open(filePath, "r") as fileRead:
            fileContents = json.load(fileRead)
        for link in fileContents["referenceLinks"]:
            if link == URL:
                links.append("https://" + file.replace("|", "/")[:len(file) - 5] + ".html")
    return links

print(get_outgoing_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))