import pymysql
import nltk


def buscaMaisPalavras(consulta):
    listacampos = 'p1.idurl'
    listatabelas = ''
    listaclausulas = ''
    palavrasid = []
    
    palavras = consulta.split(' ')
    numeroTabela = 1
    for palavra in palavras:
        idpalavra = getIdPalavra(palavra)
        if idpalavra > 1:
            palavrasid.append(idpalavra)
            if numeroTabela > 1:
                listatabelas += ', '
                listaclausulas += ' and '
                listaclausulas += 'p%d.idurl = p%d.idurl and ' % (numeroTabela -1, numeroTabela)
            listacampos += ', p%d.localizacao' % numeroTabela
            listatabelas += ' palavra_localizacao p%d' % numeroTabela
            listaclausulas += 'p%d.idpalavra = %d' % (numeroTabela, idpalavra)
            numeroTabela += 1
        consultacompleta = 'select %s from %s where %s' % (listacampos, listatabelas, listaclausulas)
        
    conexao = pymysql.connect(host='localhost', user='root', passwd='root', db='indice')
    cursor = conexao.cursor()
    cursor.execute(consultacompleta)
    linhas = [linha for linha in cursor]
    
    cursor.close()
    conexao.close()
    return linhas, palavrasid

linhas, palavrasid = buscaMaisPalavras('python programação')


def getIdPalavra(palavra):
    retorno = -1
    stemmer = nltk.stem.RSLPStemmer()
    conexao = pymysql.connect(host='localhost', user='root', passwd='root', db='indice')
    cursor = conexao.cursor()
    cursor.execute('select idpalavra from palavras where palavra = %s', stemmer.stem(palavra))
    if cursor.rowcount > 0:
        retorno = cursor.fetchone()[0]
        
    cursor.close()
    conexao.close()
    return retorno

getIdPalavra('Programação')

def buscaUmaPalavra(palavra):
    idpalavra = getIdPalavra(palavra)
    conexao = pymysql.connect(host='localhost', user='root', passwd='root', db='indice')
    cursor = conexao.cursor()
    cursor.execute('select urls.url from palavra_localizacao plc inner join urls on plc.idurl = urls.idurl where plc.idpalavra = %s', idpalavra)
    paginas = set()
    for url in cursor:
        # print(url[0])
        paginas.add(url[0])

    print('Páginas encontradas: ' + str(len(paginas)))
    for url in paginas:
        print(url)
    
    
    cursor.close()
    conexao.close()

buscaUmaPalavra('Programação')	
