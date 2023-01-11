import unidecode

def returnBagOfWords(file):
	txt = file.read().lower().replace(',', '').replace('.', '').replace('"', '')

	unaccented_string = unidecode.unidecode(txt)
	
	bagOfWords = unaccented_string.split()
	
	bagOfWords = list(set(bagOfWords))
	
	bagOfWords.sort()

	return bagOfWords

file = open("entrada2.txt", "r")

fileBagOfWords = returnBagOfWords(file)

secondFile = open("entrada3.txt", "r")

secondFileBagOfWords = returnBagOfWords(secondFile)

listOfBool = []

for termo in fileBagOfWords:
	contem = 0
	
	if (termo in secondFileBagOfWords):
		contem = 1
		
	listOfBool.append(contem)

print(listOfBool)