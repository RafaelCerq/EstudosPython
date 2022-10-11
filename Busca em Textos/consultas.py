import pymysql
import nltk


def contagemLinkScore(linhas):
    contagem = dict([linha[0], 1.0] for linha in linhas)
    conexao = pymysql.connect(host='localhost', user='root', passwd='root', db='indice')
    cursor = conexao.cursor()
    for i in contagem:
        #print(i)
        cursor.execute('select count(*) from url_ligacao where idurl_destino = %s', i)
        contagem[i] = cursor.fetchone()[0]
    
    cursor.close()
    conexao.close()
    return contagem


def distanciaScore(linhas):
    if len(linhas[0]) <= 2:
        return dict([(linha[0], 1.0) for linha in linhas])
    distancias = dict([(linha[0], 1000000) for linha in linhas])
    for linha in linhas:
        dist = sum([abs(linha[i] - linha[i -1]) for i in range(2, len(linha))])
        if dist < distancias[linha[0]]:
            distancias[linha[0]] = dist
    return distancias


distanciaScore(linhas)


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
    #scores = localizacaoScore(linhas)
    #scores = distanciaScore(linhas)
    scores = contagemLinkScore(linhas)
    
    #for linha in linhas:
    #    print(linha)
    #for url, score in scores.items():
    #    print(str(url) + ' - ' + str(score))
    
    #scoresordenado = sorted([(score, url) for (url, score) in scores.items()], reverse=0)
    scoresordenado = sorted([(score, url) for (url, score) in scores.items()], reverse=1)
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


def calculaPageRank(iteracoes):
    conexao = pymysql.connect(host='localhost', user='root', passwd='root', db='indice', autocommit = True)
    cursorLimpaTabela = conexao.cursor()
    cursorLimpaTabela.execute('delete from page_rank')
    cursorLimpaTabela.execute('insert into page_rank select idurl, 1.0 from urls')
    
    for i in range(iteracoes):
        #print("Iteracao " + str(i + 1))
        cursorUrl = conexao.cursor()
        cursorUrl.execute('select idurl from urls ')
        for url in cursorUrl:
            #print(url[0])
            pr = 0.15
            cursorLinks = conexao.cursor()
            cursorUrl.execute('select distinct(idurl_origem) from url_ligacao where idurl_destino = %s', url[0])
            for link in cursorLinks:
                cursorPageRank = conexao.cursor()
                cursorPageRank.execute('select nota from page_rank where idurl = $s', link[0])
                linkPageRank = cursorPageRank.fetchone()[0]
                cursorQuantidade = conexao.cursor()
                cursorQuantidade.execute('select count(*) from url_ligacao where idurl = %s', link[0])
                linkQuantidade = cursorQuantidade.fetchone()[0]
                pr += 0.85 * (linkPageRank / linkQuantidade)
            cursorAtualiza = conexao.cursor()
            cursorAtualiza.execute('update page_rank set nota = %s where idurl = %s', (pr, url[0]))
    
    
    cursorAtualiza.close()
    cursorQuantidade.close()
    cursorPageRank.close()
    cursorLinks.close()
    cursorUrl.close()
    cursorLimpaTabela.close()
    conexao.close()

