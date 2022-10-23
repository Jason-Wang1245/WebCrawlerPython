import math
import os
import searchdata
        
# altered selection sort to sort top 10 (or all of the list if length of list is less than 10) based on consine similarity scores
def selectionSort(list):
    start = 0
    if len(list) < 10:
        listMax = len(list)
    else:
        listMax = 10
    while start < listMax:
        for i in range(start, len(list)):
            if list[i]["score"] > list[start]["score"]:
                list[i], list[start] = list[start], list[i]
        start += 1
    return list[0:listMax]

def search(phrase, boost):
    # final list to be returned
    searchResults = []
    # create lists needed for creating page and query vectors
    vectorOrder = []
    queryVector = []
    # left portion of the denominator when calculating cosine similarity
    queryDenominator = 0
    phraseSplit = phrase.strip().lower().split()
    words = {}
    # counts the occurence of each word and stores it in words
    for word in phraseSplit:
        if not word in words:
            words[word] = phraseSplit.count(word)
    # generates the order of the vector to be used when making each page vector, queryDenominator, and the queryVector to be used to calculate the numerator of the cosine similarity equation
    for word in words:
        idf = searchdata.get_idf(word)
        # this skips words in the query that do not exist in crawled pages
        if idf != 0:
            queryTfidf = math.log(1 + (words[word] / len(phraseSplit)), 2) * idf
            queryVector.append(queryTfidf)
            vectorOrder.append(word)
            queryDenominator += queryTfidf ** 2
    queryDenominator = queryDenominator ** (1 / 2)
    # gets every webpage data folder in order to generate cosine similarities to the query vector
    pageFolders = os.listdir("pageData")
    for folder in pageFolders:
        url = "http://" + folder.replace("}", "/").rstrip(".json")
        pageDenominator = 0
        numerator = 0
        # generates rest of the values needed to calculate cosine similarity
        for i in range(len(vectorOrder)):
            pageTfIdf = searchdata.get_tf_idf(url, vectorOrder[i])
            numerator += pageTfIdf * queryVector[i]
            pageDenominator += pageTfIdf ** 2
        
        if pageDenominator == 0:
            cosineSimilaritiy = 0
        else:
            cosineSimilaritiy = numerator / (queryDenominator * (pageDenominator ** (1 / 2)))
            if boost:
                cosineSimilaritiy *= searchdata.get_page_rank(url)
        
        searchResults.append({"url": url, "title": searchdata.get_title(url), "score": cosineSimilaritiy})

    return selectionSort(searchResults)