import pandas as pd

docGerado = pd.read_csv('responseClassificado.csv',
                        sep='|',
                        usecols=['Tweet', 'Classificação'])
docEspecialista = pd.read_csv('reforma_previdencia_rotulado.csv',
                              sep=';',
                              usecols=['Tweet', 'Classificação'])

neutros = 0
negativos = 0
positivos = 0
neutrosErrados = 0
negativosErrados = 0
positivosErrados = 0

for index, row in docEspecialista.iterrows():
    sentimentEspec = docEspecialista.iloc[index]['Classificação']
    sentimentGerado = docGerado.iloc[index]['Classificação']
    if sentimentEspec == "Neutro":
        neutros += 1
        if sentimentEspec != sentimentGerado:
            neutrosErrados += 1

    if sentimentEspec == "Positivo":
        positivos += 1
        if sentimentEspec != sentimentGerado:
            positivosErrados += 1

    if sentimentEspec == "Negativo":
        negativos += 1
        if sentimentEspec != sentimentGerado:
            negativosErrados += 1

print("Quantidades por classe: ")
print(f"Neutros: {neutros}")
print(f"Positivos: {positivos}")
print(f"Negativos: {negativos}")
print("Quantidade de erros por classe: ")
print(f"Neutros: {neutrosErrados}")
print(f"Positivos: {positivosErrados}")
print(f"Negativos: {negativosErrados}")
print("Percentual de erros class: ")

if neutros > 0:
    print(f"Neutros: {(neutrosErrados/neutros)*100}%")
else:
    print(f"Neutros: 0.0%")
if positivos > 0:
    print(f"Positivos: {(positivosErrados/positivos)*100}%")
else:
    print(f"Positivos: 0.0%")
if negativos > 0:
    print(f"Negativos: {(negativosErrados/negativos)*100}%")
else:
    print(f"Negativos: 0.0%")