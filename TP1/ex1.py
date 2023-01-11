import unidecode

file = open("entrada.txt", "r")

txt = file.read().lower().replace(',', '').replace('.', '').replace('"', '')

unaccented_string = unidecode.unidecode(txt)

bagOfWords = unaccented_string.split()

bagOfWords = list(set(bagOfWords))

bagOfWords.sort()

fileSaida = open("saida.txt", 'w')
  
for word in bagOfWords:
	fileSaida.write(str(word) + '\n')

fileSaida.close()