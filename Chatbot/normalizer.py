def textNormalizer(userInput): 
    def wordNormalizer(word):
        word = word.lower()
        word = list(word)
        validLetters = [chr(i) for i in range(97,133)]
        validLetters.append("-")
        validLetters.append("'")
        validLetters.append("’")
        newWordList = [i for i in word if i in validLetters]
        return "".join(newWordList)

    def wordStorage(data):
        normalizedWordList = []
        words = data.split()
        for word in words:
            word = wordNormalizer(word)
            normalizedWordList.append(word)
        return normalizedWordList
    
    def combinationOfWords(inputList):
        newList = inputList.copy()
        
        for terms in range(2,5):
            i = 0
            while True:
                try:
                    combinedWord = inputList[i] + " "
                    for j in range(1,terms):
                        combinedWord += inputList[i + j]+" "
                    newList.append(combinedWord.strip())
                    i += 1
                except:
                    break
        return newList
    
    return combinationOfWords(wordStorage(userInput))
