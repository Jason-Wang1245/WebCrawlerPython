import math

def search(phrase, boost):
    # gets idf values and vector indices
    fileRead = open(os.path.join("otherData", "idf.json"), "r")
    idfData = json.load(fileRead)
    fileRead.close()
    
    
    words = phrase.strip().split()
    vectorOrder = []
    queryVector = [0] * len(words)
    for word in words:
        if word in idfData:
            queryVector.append(math.log(1 + (1 / len(words)), 2) * idfData[word][1])
            vectorOrder.append(word)
    
    pageFiles = os.listdir("pageData")

    for file in pageFiles:
        fileRead = open(os.path.join("pageData", file), "r")
        pageData = json.load(fileRead)
        paegVector = []
        
        
