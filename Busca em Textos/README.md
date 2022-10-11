# EstudosPython

## Parte do estudo foi utilizando Anaconda (Spyder)

### Instalação biblioteca utilizada na buscas em textos
- conda install urllib3

### Instalação biblioteca utilizada na extração de dados
- conda install beautifulsoup4

### Instalação biblioteca para conectar e executar comandos no mysql
- conda install pymysql


## Resumo de métricas (Exemplo: Pesquisando pela palavra python)
### Frequência
- Se for um artigo sobre Python terá mais repetições e evitará alguém que citou Python uma só vez e não era sobre a linguagem
### Posição
- Se a página for relevante, os termos aparecerão perto do início ou mesmo no título.
- Mais difícil de ser enganada do que frequência, pois se os autores colocarem as palavras no início e repetir não afetará os resultados.
### Distância
- Quando tem muitas palavras na pesquisa é útil procurar resultados que elas aparecem mais próximas
- Quando são feitas buscas com mais de uma palavra a ideia é relacionar os termos
### PageRank
- Nota baseada na importância da página (nota PageRank) e na quantidade de links
- Páginas citadas por páginas importantes também podem ser importantes
### Texto do link
- Muitas vezes o link mostra informações melhores do que o conteúdo da página
- Combinação com o PageRank