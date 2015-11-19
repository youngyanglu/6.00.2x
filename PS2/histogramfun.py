import matplotlib.pyplot as plt

WORDLIST_FILENAME = "/Users/Young/Dropbox/datajoy/6.00.2x/PS2/words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of uppercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def plotVowelProportionHistogram(wordList, numBins=15):
    """
    Plots a histogram of the proportion of vowels in each word in wordList
    using the specified number of bins in numBins
    """
    numvowel=[]
    vowels = "aeiou"
    for word in wordList:
        for v in vowels:
            lens=float(len(word))
            num= word.lower().count(v)/lens
            numvowel.append(num)
    print numvowel
    plt.hist(numvowel, numBins)
    plt.show()
    
if __name__ == '__main__':
    wordList = loadWords()
    plotVowelProportionHistogram(wordList)