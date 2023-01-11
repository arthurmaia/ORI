# python main.py /home/runner/ORI/TP3/vocabulary.txt /home/runner/ORI/TP3/docs /home/runner/ORI/TP3/query.txt

import sys
import os
import unidecode
import math

class Document:
	name = ''
	bow = []
	standard = 0.0
	similarity = 0.0

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

def calcStandardFromDocument(document, listOfTerms):
	sum = 0.0

	termsFromCurrentDocument = []

	for term in listOfTerms:
		if term.document == document:
			termsFromCurrentDocument.append(term)

	for term in termsFromCurrentDocument:
		sum += (term.tf_idf ** 2)

	return math.sqrt(sum)

def calcQueryStandard(query, listOfTerms):
	sum = 0.0

	listOfQueryTerms = []

	for qTerm in query:
		for term in listOfTerms:
			if (term.term == qTerm):
				listOfQueryTerms.append(term)
				break

	for term in listOfQueryTerms:
		sum += (term.idf ** 2)

	return math.sqrt(sum)

def getTermIndexFromName(name, listOfTerms):
	index = -1

	for i, term in enumerate(listOfTerms):
		if term.term == name:
			index = i

	return index

def calcSimilarityFromDocument(documentName, documentStandard, queryStandard, query, listOfTerms):
	termsFromDocument = []
	listOfQueryTerms = []

	for qTerm in query:
		for term in listOfTerms:
			if (term.term == qTerm):
				listOfQueryTerms.append(term)
				break

	for term in listOfTerms:
		if term.document == documentName:
			termsFromDocument.append(term)

	dottedValue = 0.0

	for docTerm in termsFromDocument:
		index = getTermIndexFromName(docTerm.term, listOfQueryTerms)
		if index != -1:
			queryTerm = listOfQueryTerms[index]
			dottedValue += (docTerm.tf_idf * queryTerm.idf)
	
	result = dottedValue / (documentStandard * queryStandard)
	
	return result

vocabularyPath = sys.argv[1]
folderPath = sys.argv[2]
queryPath = sys.argv[3]

vocabularyFileName = vocabularyPath.split('/')[-1]
queryFileName = queryPath.split('/')[-1]

os.chdir(folderPath)

documents = []
documentsLength = 0

for file in os.listdir():
	if file.endswith('.txt') and file != vocabularyFileName and file != queryFileName:
		documentsLength += 1
		file_path = f"{folderPath}/{file}"
		
		boW = returnBoWFromFilePath(file_path)

		document = Document()

		document.name = file.replace('.txt', '')
		document.bow = boW
		
		documents.append(document)

vocabulary = returnBoWFromFilePath(vocabularyPath)
query = returnBoWFromFilePath(queryPath)

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

queryStandard = calcQueryStandard(query, listOfTerm)

for document in documents:
	standard = calcStandardFromDocument(document.name, listOfTerm)
	document.standard = standard
	document.similarity = calcSimilarityFromDocument(document.name, standard, queryStandard, query, listOfTerm)
	
documents.sort(key=lambda x: x.similarity, reverse=True)
							 
for document in documents:
	print(f'Documento {document.name} - Grau de Similaridade {document.similarity}')
