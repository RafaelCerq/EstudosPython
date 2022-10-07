import re
import nltk # biblioteca para processamento de linguagem natural

### Ao utilizar a biblioteca de linguagem natural NLTK, execute a linha abaixo para instalar os pacotes
nltk.download()

stop1 = ['é']
stop2 = nltk.corpus.stopwords.words('portuguese')
stop2
stop2.append('é')

# \\W+ indica que pode ter palavra seguida de outros elementos
splitter = re.compile('\\W+')
stemmer = nltk.stem.RSLPStemer()
lista_palavras = []
lista = [p for p in splitter.split('Este lugar é apavorante a b c') if p != '' ]
for p in lista:
    if p.lower() not in stop2:
        if len(p) > 1:
            lista_palavras.append(stemmer.stem(p).lower())
            
            
stemmer.stem('nova')
stemmer.stem('novamente')

