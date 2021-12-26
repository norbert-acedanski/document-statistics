import matplotlib.pyplot as plt
import re

fileName = "processFile.txt"
startIndex = 0
amountOfWordsToDisplay = 100

def loadData():
    global data
    with open(fileName, "r", encoding='utf-8') as inputFile:
        data = inputFile.readlines()
        for (lineNumber, line) in enumerate(data):
            data[lineNumber] = line.replace('\n', '')
    return data

def processData(data):
    wordCount = {}
    for line in data:
        for word in line.split():
            isolatedWord = re.sub('[!?@#$\[\]<>%^&*()]', '', word).lower()
            isolatedWord = isolatedWord.replace(',', '.') if ',' in isolatedWord else isolatedWord
            try:
                wordWithNumbersHandled = float(isolatedWord)
            except:
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

def plotZipf(wordsList, numberOfWordInstancesList):
    for (number, word) in enumerate(wordsList):
        wordsList[number] = str(number + 1) + ". " + str(word)
    plt.figure("Zipf Graph")
    plt.title("Zipf Graph")
    plt.xlabel("Word in given document")
    plt.ylabel("Amount of times the word occurs in the document")
    plt.plot(wordsList[startIndex: startIndex + amountOfWordsToDisplay], numberOfWordInstancesList[startIndex: startIndex + amountOfWordsToDisplay])
    plt.xticks(rotation=90)
    plt.show()

if __name__ == '__main__':
    data = loadData()
    wordsList, numberOfWordInstancesList = processData(data)
    saveToFiles(wordsList, numberOfWordInstancesList)
    plotZipf(wordsList, numberOfWordInstancesList)