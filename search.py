def search(phrase, boost):
    words = phrase.strip().split()
    pageFiles = os.listdir("pageData")
    for file in pageFiles:
        