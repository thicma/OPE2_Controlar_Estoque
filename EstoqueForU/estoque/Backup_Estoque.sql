--
-- File generated with SQLiteStudio v3.3.0 on seg abr 26 21:14:21 2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: autorizacao
CREATE TABLE autorizacao (
	id INTEGER NOT NULL, 
	descricao VARCHAR(15), 
	PRIMARY KEY (id)
);

-- Table: fornecedor
CREATE TABLE fornecedor (
	id INTEGER NOT NULL, 
	name VARCHAR(30) NOT NULL, 
	email VARCHAR(50) NOT NULL, 
	fone VARCHAR(15) NOT NULL, 
	cnpj VARCHAR(14) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	UNIQUE (email), 
	UNIQUE (cnpj)
);
INSERT INTO fornecedor (id, name, email, fone, cnpj) VALUES (1, 'Fornece Tudo', 'fornece_tudo@gmail.com', '1199990000', '10123456000110');
INSERT INTO fornecedor (id, name, email, fone, cnpj) VALUES (2, 'Bom Fornecedor', 'bom_fornecedor@gmail.com', '1188881111', '11123456000220');
INSERT INTO fornecedor (id, name, email, fone, cnpj) VALUES (3, 'Quero Roupa', 'quero_roupa@hotmail.com', '1177772222', '12123456000330');

-- Table: marca
CREATE TABLE marca (
	nome VARCHAR(20) NOT NULL, 
	id INTEGER NOT NULL, 
	fornecedor INTEGER NOT NULL, 
	PRIMARY KEY (nome)
);
INSERT INTO marca (nome, id, fornecedor) VALUES ('Nova Roupa', 1, 1);
INSERT INTO marca (nome, id, fornecedor) VALUES ('Uahau Roupa', 6, 3);
INSERT INTO marca (nome, id, fornecedor) VALUES ('A Roupa Nova do Rei', 5, 1);
INSERT INTO marca (nome, id, fornecedor) VALUES ('Bonitas Roupas', 4, 3);
INSERT INTO marca (nome, id, fornecedor) VALUES ('Roupa Nova', 3, 2);
INSERT INTO marca (nome, id, fornecedor) VALUES ('Minha Calça', 2, 2);

-- Table: produto
CREATE TABLE produto (
	id INTEGER NOT NULL, 
	tipo VARCHAR(15) NOT NULL, 
	descricao VARCHAR(50) NOT NULL, 
	modelo VARCHAR(20) NOT NULL, 
	ano_colecao INTEGER NOT NULL, 
	material VARCHAR(20) NOT NULL, 
	cor VARCHAR(15) NOT NULL, 
	preco FLOAT NOT NULL, 
	quantidade INTEGER NOT NULL, 
	marca_nome VARCHAR(20), 
	tamanho_id VARCHAR(2), 
	PRIMARY KEY (id), 
	FOREIGN KEY(marca_nome) REFERENCES marca (nome), 
	FOREIGN KEY(tamanho_id) REFERENCES tamanho (id)
);
INSERT INTO produto (id, tipo, descricao, modelo, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (1, 'Calça', 'Calça Jeans de Cintura Baixa', 'Cintura Baixa', 2021, 'Jeans', 'Branca', 59.9, 10, 'Nova Roupa', 'G');
INSERT INTO produto (id, tipo, descricao, modelo, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (2, 'Calça', 'Calça de Moleton', 'Esporte', 2020, 'Moleton', 'Azul', 29.9, 20, 'Uahau Roupa', 'M');
INSERT INTO produto (id, tipo, descricao, modelo, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (3, 'Calça', 'Calça de Moleton', 'Esporte', 2020, 'Moleton', 'Branca', 40.9, 5, 'Uahau Roupa', 'M');
INSERT INTO produto (id, tipo, descricao, modelo, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (4, 'Calça', 'Calça de Moleton', 'Treino', 2021, 'Moleton', 'Preta', 60.5, 4, 'A Roupa Nova do Rei', 'P');

-- Table: tamanho
CREATE TABLE tamanho (
	id VARCHAR(2) NOT NULL, 
	descricao VARCHAR(15) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO tamanho (id, descricao) VALUES ('GG', 'Extra Grande');
INSERT INTO tamanho (id, descricao) VALUES ('G', 'Grande');
INSERT INTO tamanho (id, descricao) VALUES ('M', 'Médio');
INSERT INTO tamanho (id, descricao) VALUES ('P', 'Pequeno');
INSERT INTO tamanho (id, descricao) VALUES ('PP', 'Muito Pequeno');

-- Table: tipo
CREATE TABLE tipo (
	id INTEGER NOT NULL, 
	descricao VARCHAR(50) NOT NULL, 
	material VARCHAR(20) NOT NULL, 
	modelo VARCHAR(20) NOT NULL, 
	ano_colecao INTEGER NOT NULL, 
	PRIMARY KEY (id)
);

-- Table: transacao
CREATE TABLE transacao (
	id INTEGER NOT NULL, 
	data DATETIME NOT NULL, 
	user_id INTEGER, 
	produto_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(produto_id) REFERENCES produto (id)
);

-- Table: user
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(30) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	charge VARCHAR(50) NOT NULL, 
	password_hash VARCHAR(60) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
INSERT INTO user (id, username, name, charge, password_hash) VALUES (1, 'thiago', 'Thiago Carlos Mendes de Andrade', 'gerente', '$2b$12$3u5Cih1W..h8JEWML4OeaeLT1K3.fNi1FFPMDWTsChglH5JYEZHaO');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
