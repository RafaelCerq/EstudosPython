create database indice character set=utf8mb4 collate=utf8mb4_unicode_ci;
use indice;

create table urls (
	idurl int not null auto_increment,
	url varchar(1000) not null,
	constraint pk_urls_idurl primary key (idurl)
);

-- create index idx_urls_url on urls (url);

create table palavras (
	idpalavra int not null auto_increment,
	palavra varchar(200) character set utf8mb4 collate utf8mb4_unicode_ci not null,
	constraint pk_palavras_palavra primary key (idpalavra)
) character set utf8mb4 collate utf8mb4_unicode_ci;

create index idx_palavras_palavra on palavras (palavra);

create table palavra_localizacao (
	idpalavra_localizacao int not null auto_increment,
	idurl int not null,
	idpalavra int not null,
	localizacao int,
	constraint pk_idpalavra_localizacao primary key (idpalavra_localizacao),
	constraint fk_palavra_localizacao_idurl foreign key (idurl) references urls (idurl),
	constraint fk_palavra_localizacao_idpalavra foreign key (idpalavra) references palavras (idpalavra)
);

create index idx_palavra_localizacao_idpalavra on palavra_localizacao (idpalavra);

