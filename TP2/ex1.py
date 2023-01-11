import sys
import os
import unidecode

class Document:
	name = ''
	bow = []

def returnBoWFromFilePath(path):
	file = open(path, "r")

	txt = file.read().lower().replace(',', '').replace('.', '').replace('"', '').replace('!', '').replace('?', '').replace('(', '').replace(')', '')
	
	unaccented_string = unidecode.unidecode(txt)
	
	bagOfWords = unaccented_string.split()
	
	bagOfWords.sort()

	return bagOfWords

folderPath = sys.argv[1]

vocabularyFileName = "vocabulary.txt"
finalFileName = "result.txt"

os.chdir(folderPath)

vocabulary = []
documents = []

for file in os.listdir():
	if file.endswith('.txt') and file != vocabularyFileName and file != finalFileName:
		file_path = f"{folderPath}/{file}"
		boW = returnBoWFromFilePath(file_path)

		document = Document()

		document.name = file.replace('.txt', '')
		document.bow = boW
		
		documents.append(document)
		
		vocabulary = [*vocabulary, *boW]

vocabulary = list(set(vocabulary))

fileSaida = open(vocabularyFileName, 'w')
  
for word in vocabulary:
	fileSaida.write(str(word) + '\n')

fileSaida.close()

finalFile = open(finalFileName, 'w')

for term in vocabulary:
	finalFile.write(f'Termo: {term}\n')

	for document in documents:
		includedCounter = document.bow.count(term)

		finalFile.write(f'{document.name}: {includedCounter}\n')

	finalFile.write('\n')

finalFile.close()