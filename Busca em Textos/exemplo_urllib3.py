import urllib3

http = urllib3.PoolManager()
pagina = http.request('GET', 'http://www.iaexpert.com.br')

#verifica status da pagina
pagina.status

# Exibe todo html da pagina
pagina.data

#Exibe os caractares ente os valores informados
pagina.data[0:50]
