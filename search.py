import math
import os
import searchdata
        
def selectionSort(list):
    start = 0
    while start < len(list):
        for i in range(start, len(list)):
            if list[i]["score"] > list[start]["score"]:
                list[i], list[start] = list[start], list[i]
        start += 1
    return list


def search(phrase, boost):
    searchResults = []

    vectorOrder = []
    queryVector = []
    queryDenominator = 0
    phraseSplit = phrase.strip().lower().split()
    words = {}
    for word in phraseSplit:
        if not word in words:
            words[word] = phraseSplit.count(word)
    for word in words:
        idf = searchdata.get_idf(word)
        if idf != 0:
            queryTfidf = math.log(1 + (words[word] / len(phraseSplit)), 2) * idf
            queryVector.append(queryTfidf)
            vectorOrder.append(word)
            queryDenominator += queryTfidf ** 2
    queryDenominator = queryDenominator ** (1 / 2)
    # gets every webpage data file in order to generate cosine similarities to the query vector
    pageFiles = os.listdir("pageData")
    for file in pageFiles:
        url = "http://" + file.replace("}", "/").rstrip(".json")
        pageDenominator = 0
        numerator = 0
        pageVector = []
        # generates a vector space model for the current webpage data file
        for i in range(len(vectorOrder)):
            pageTfIdf = searchdata.get_tf_idf(url, vectorOrder[i])
            pageVector.append(pageTfIdf)
            numerator += pageTfIdf * queryVector[i]
            pageDenominator += pageTfIdf ** 2
        
        if pageDenominator == 0:
            cosineSimilaritiy = 0
        else:
            cosineSimilaritiy = numerator / (queryDenominator * (pageDenominator ** (1 / 2)))
            if boost:
                cosineSimilaritiy *= searchdata.get_page_rank(url)
        searchResults.append({"url": url, "title": searchdata.get_title(url), "score": cosineSimilaritiy})

    searchResults = selectionSort(searchResults)

    if len(searchResults) > 10:
        rankAmount = 10
    else:
        rankAmount = len(searchResults)

    return searchResults[0:rankAmount]

        
