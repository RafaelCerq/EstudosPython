import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Criando metodo crawl
def crawl(paginas, profundidade):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning())
    for i in range(profundidade):
        novas_paginas = set();
        
        for pagina in paginas:
        
            http = urllib3.PoolManager()
             
            try:
                dados_pagina = http.request('GET', pagina)
            except:
                print('Erro ao Abrir a pagina ' + pagina)
                continue
                
            
            sopa = BeautifulSoup(dados_pagina.data, "lxml")
            links = sopa.find_all('a')
            contador = 1
            for link in links:
                #print(str(link.contents) + " - " + str(link.get('href')))
                #print(link.attrs)
                #print('\n')
                
                if ('href' in link.attrs):
                    url = urljoin(pagina, str(link.get('href')))
                    #if url != link.get('href'):
                        #print(url)
                        #print(link.get('href'))
                        
                    if url.find("'") != -1:
                        continue
                    
                    #print(url)
                    url = url.split('#')[0]
                    #print(url)
                    #print('\n')
                    
                    if url[0:4] == 'http':
                        novas_paginas.add(url);
        
                    contador = contador + 1
            
            paginas = novas_paginas
            print(contador)
        
        
listapaginas = ['https://pt.wikipedia.org/wiki/Linguagem_de_programa%C3%A7%C3%A3o']
# Incluir profundidade 2 para incluir os links encontrados na primeira etapa
crawl(listapaginas, 1)
