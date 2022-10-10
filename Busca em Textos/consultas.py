import pymysql
import nltk


def localizacaoScore(linhas):
    localizacoes = dict([linha[0], 1000000] for linha in linhas)
    for linha in linhas:
        soma = sum(linha[1:])
        if soma < localizacoes[linha[0]]:
            localizacoes[linha[0]] = soma
    return localizacoes


localizacaoScore(linhas)


def frequenciaScore(linhas):
    contagem = dict([linha[0], 0] for linha in linhas)
    for linha in linhas:
        contagem[linha[0]] += 1
        #print(linha)
    return contagem

frequenciaScore(linhas)

def pesquisa(consulta):
    linhas, palavrasid = buscaMaisPalavras(consulta)
    #linhas, palavrasid = buscaMaisPalavras('python programação')
    
    #scores = dict([linha[0],0] for linha in linhas)
    #scores = frequenciaScore(linhas)
    scores = localizacaoScore(linhas)
    
    #for linha in linhas:
    #    print(linha)
    #for url, score in scores.items():
    #    print(str(url) + ' - ' + str(score))
    scoresordenado = sorted([(score, url) for (url, score) in scores.items()], reverse=0)
    for (score, idurl) in scoresordenado[0:10]:
        print('%f\t%s' % (score, getUrl(idurl)))

pesquisa('python programação')


def getUrl(idurl):
    retorno = ''
    conexao = pymysql.connect(host='localhost', user='root', passwd='root', db='indice')
    cursor = conexao.cursor()
    cursor.execute('select url from urls where idurl = %s', idurl)
    if cursor.rowcount > 0:
        retorno = cursor.fetchone()[0]
    
    cursor.close()
    conexao.close()
    return retorno

getUrl(1)


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
