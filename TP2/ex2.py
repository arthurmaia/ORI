import sys
import os
import unidecode
import math

class Document:
	name = ''
	bow = []

class Term:
	term = ''
	frequency = 0
	document = ''
	tf = 0.0
	idf = 0.0
	tf_idf = 0.0

class NI:
	term = ''
	ni = 0

def returnBoWFromFilePath(path):
	file = open(path, "r")

	txt = file.read().lower().replace(',', '').replace('.', '').replace('"', '').replace('!', '').replace('?', '').replace('(', '').replace(')', '')
	
	unaccented_string = unidecode.unidecode(txt)
	
	bagOfWords = unaccented_string.split()

	return bagOfWords

vocabularyPath = sys.argv[1]
folderPath = sys.argv[2]

vocabularyFileName = vocabularyPath.split('/')[-1]

os.chdir(folderPath)

documents = []
documentsLength = 0

for file in os.listdir():
	if file.endswith('.txt') and file != vocabularyFileName:
		documentsLength += 1
		file_path = f"{folderPath}/{file}"
		
		boW = returnBoWFromFilePath(file_path)

		document = Document()

		document.name = file.replace('.txt', '')
		document.bow = boW
		
		documents.append(document)

vocabulary = returnBoWFromFilePath(vocabularyFileName)

listOfTerm = []

for term in vocabulary:
	for document in documents:
		frequency = Term()

		frequencyCounter = document.bow.count(term)

		frequency.term = term
		frequency.frequency = frequencyCounter
		frequency.document = document.name

		if (frequencyCounter > 0):
			frequency.tf = float(1 + math.log2(frequencyCounter))

		listOfTerm.append(frequency)

listOfNI = []

for term in vocabulary:
	ni = NI()

	ni.term = term

	counter = 0

	for item in listOfTerm:
		if (item.term == term):
			if (item.frequency > 0):
				counter += 1

	ni.ni = counter

	listOfNI.append(ni)

for item in listOfTerm:
	ni = 0

	for item_ni in listOfNI:
		if (item_ni.term == item.term):
			ni = item_ni.ni

	if ni > 0:
		item.idf = math.log2(documentsLength / ni)

for item in listOfTerm:
	item.tf_idf = item.tf * item.idf

for term in listOfTerm:
	print(f'TF-IDF({term.term}, {term.document}) = {term.tf_idf}')