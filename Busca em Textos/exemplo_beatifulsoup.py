#Tag soup
from bs4 import BeautifulSoup
import urllib3

# Desabilitar warning segurança de certificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning())
http = urllib3.PoolManager()
#pagina = http.request('GET', 'http://www.iaexpert.com.br')
pagina = http.request('GET', 'https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o')
pagina.status

# armazena na variavel todos os dados da página em formato lxml
sopa = BeautifulSoup(pagina.data, 'lxml')

sopa

# Exibindo tag e conteúdo titulo da pagina
sopa.title

# Exibindo conteúdo titulo da pagina sem tag
sopa.title.string

# armazenando na variavel links todas as tags 'a' (que geralmente contem links)
links = sopa.find_all('a')

# Exibindo tamanho/quantos itens tem na variavel
len(links)

# for para exibir os nomes e links descritos em 'href' das tags 'a'
for link in links:
    print(link.get('href'))
    print(link.content)
