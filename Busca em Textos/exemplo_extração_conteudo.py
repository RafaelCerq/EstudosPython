import urllib3
from bs4 import BeautifulSoup

http = urllib3.PoolManager()
pagina = http.request('GET', 'https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o')


sopa = BeautifulSoup(pagina.data, 'lxml')

# removendo conteudo de extração 
for tags in sopa(['script', 'style']):
    tags.decompose()

# stripped_strings remove todos os espaços em branco
conteudo = ' '.join(sopa.stripped_strings)
