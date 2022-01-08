import matplotlib.pyplot as plt
import re
import sys

fileName = "processFile.txt"
startIndex = 0
amountOfWordsToDisplay = 100

def loadData():
    global data
    try:
        with open(fileName, "r", encoding='utf-8') as inputFile:
            data = inputFile.readlines()
            for (lineNumber, line) in enumerate(data):
                data[lineNumber] = line.replace('\n', '')
    except OSError:
        print("File \"" + fileName + "\" could not be opened. Check file name or file path.")
        sys.exit()
    if len(data) == 0:
        print("No data found in given a file!")
        sys.exit()
    return data

def processData(data):
    wordCount = {}
    for line in data:
        for word in line.split():
            isolatedWord = re.sub('[!?@#$\[\]<>%^&*()]', '', word).lower()
            isolatedWord = isolatedWord.replace(',', '.') if ',' in isolatedWord else isolatedWord
            try:
                wordWithNumbersHandled = float(isolatedWord)
            except ValueError:
                wordWithNumbersHandled = re.sub('[,.]', '', isolatedWord)

            if wordWithNumbersHandled in wordCount:
                wordCount[str(wordWithNumbersHandled)] += 1
            else:
                wordCount[str(wordWithNumbersHandled)] = 1
    sortedWordCount = sorted(wordCount.items(), key=lambda x: x[1], reverse=True)
    wordsList, numberOfWordInstancesList = [], []
    for pair in sortedWordCount:
        wordsList.append(pair[0])
        numberOfWordInstancesList.append(pair[1])
    return wordsList, numberOfWordInstancesList

def saveToFiles(wordsList, numberOfWordInstancesList):
    with open("wordsList.txt", "w", encoding='utf-8') as wordsListFile, open("numberOfWordInstancesList.txt", "w", encoding='utf-8') as numberOfWordInstancesListFile:
        for count in range(len(wordsList)):
            wordsListFile.write(wordsList[count] + '\n')
            numberOfWordInstancesListFile.write(str(numberOfWordInstancesList[count]) + '\n')

def printNumberOfWordsInGivenFile():
    print("Number of words in a given file: " + str(len(wordsList)))

def plotZipf(wordsList, numberOfWordInstancesList):
    for (number, word) in enumerate(wordsList):
        wordsList[number] = str(number + 1) + ". " + str(word)
    contunueGraph = "y"
    multiplyFactor = 1
    plt.figure("Zipf Graph")
    plt.ion()
    plt.show()
    while contunueGraph == "y":
        if startIndex + (multiplyFactor - 1)*amountOfWordsToDisplay > len(wordsList):
            print("No more words to graph")
            input("To close window, press Enter")
            break
        plt.clf()
        plt.title("Zipf Graph")
        plt.xlabel("Word in given document")
        plt.ylabel("Amount of times the word occurs in the document")
        plt.plot(wordsList[startIndex + (multiplyFactor - 1)*amountOfWordsToDisplay: startIndex + multiplyFactor*amountOfWordsToDisplay], numberOfWordInstancesList[startIndex + (multiplyFactor - 1)*amountOfWordsToDisplay: startIndex + multiplyFactor*amountOfWordsToDisplay], marker= "o")
        plt.xticks(rotation=90)
        plt.grid(True)
        plt.draw()
        contunueGraph = input("Show next " + str(amountOfWordsToDisplay) + " words? (y/N): ").lower()
        while contunueGraph != "y" and contunueGraph != "n":
            contunueGraph = input("Unknown command. Try again!: ")
        multiplyFactor += 1
    print("Closing window")

if __name__ == '__main__':
    data = loadData()
    wordsList, numberOfWordInstancesList = processData(data)
    saveToFiles(wordsList, numberOfWordInstancesList)
    printNumberOfWordsInGivenFile()
    plotZipf(wordsList, numberOfWordInstancesList)