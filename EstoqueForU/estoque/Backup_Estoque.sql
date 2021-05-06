--
-- File generated with SQLiteStudio v3.3.0 on ter mai 4 10:04:36 2021
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

-- Table: categoria
CREATE TABLE categoria (id INTEGER NOT NULL, descricao VARCHAR (50) NOT NULL, PRIMARY KEY (id));
INSERT INTO categoria (id, descricao) VALUES (1, 'blusa');
INSERT INTO categoria (id, descricao) VALUES (2, 'calça');
INSERT INTO categoria (id, descricao) VALUES (3, 'camisa');
INSERT INTO categoria (id, descricao) VALUES (4, 'camiseta');
INSERT INTO categoria (id, descricao) VALUES (5, 'casaco');
INSERT INTO categoria (id, descricao) VALUES (6, 'esporte');
INSERT INTO categoria (id, descricao) VALUES (7, 'fitness');
INSERT INTO categoria (id, descricao) VALUES (8, 'macacao');
INSERT INTO categoria (id, descricao) VALUES (9, 'moda íntima');
INSERT INTO categoria (id, descricao) VALUES (10, 'moda praia');
INSERT INTO categoria (id, descricao) VALUES (11, 'saia');
INSERT INTO categoria (id, descricao) VALUES (12, 'shorts');
INSERT INTO categoria (id, descricao) VALUES (13, 'vestido');

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
INSERT INTO marca (nome, id, fornecedor) VALUES ('nova roupa', 1, 1);
INSERT INTO marca (nome, id, fornecedor) VALUES ('uahau roupa', 6, 3);
INSERT INTO marca (nome, id, fornecedor) VALUES ('a roupa nova do rei', 5, 1);
INSERT INTO marca (nome, id, fornecedor) VALUES ('bonitas roupas', 4, 3);
INSERT INTO marca (nome, id, fornecedor) VALUES ('roupa nova', 3, 2);
INSERT INTO marca (nome, id, fornecedor) VALUES ('minha calça', 2, 2);

-- Table: produto
CREATE TABLE produto (id INTEGER NOT NULL, tipo_id VARCHAR (15) NOT NULL CONSTRAINT tipo_id REFERENCES categoria (id), descricao VARCHAR (50) NOT NULL, modelo VARCHAR (20) NOT NULL, genero VARCHAR (8, 9), ano_colecao INTEGER NOT NULL, material VARCHAR (20) NOT NULL, cor VARCHAR (15) NOT NULL, preco FLOAT NOT NULL, quantidade INTEGER NOT NULL, marca_nome VARCHAR (20), tamanho_id VARCHAR (2), PRIMARY KEY (id), FOREIGN KEY (marca_nome) REFERENCES marca (nome), FOREIGN KEY (tamanho_id) REFERENCES tamanho (id));
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (1, '2', 'Calça Jeans de Cintura Baixa', 'Cintura Baixa', 'feminino', 2021, 'jeans', 'branca', 59.9, 10, 'nova roupa', 'm');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (2, '2', 'Calça de Moleton', 'Esporte', 'masculino', 2020, 'moleton', 'azul', 29.9, 20, 'uahau roupa', 'gg');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (3, '2', 'Calça de Moleton', 'Esporte', 'masculino', 2020, 'moleton', 'branca', 40.9, 5, 'uahau roupa', 'g');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (4, '2', 'Calça de Moleton', 'Treino', 'feminino', 2021, 'moleton', 'preta', 60.5, 4, 'nova roupa', 'g');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (5, '1', 'blusa manga longa com gola v', 'gola v', 'masculino', 2020, 'algodão', 'preta', 29.9, 10, 'nova roupa', 'gg');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (6, '4', 'camiseta manga curta', 'regata', 'feminino', 2021, 'algodão', 'estampada', 15.95, 10, 'nova roupa', 'pp');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (7, '12', 'shorts para prática de esportes', 'esporte', 'masculino', 2021, 'poliester', 'estampada', 19.99, 10, 'bonitas roupas', 'p');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (8, '4', 'camiseta manga longa', 'manga longa', 'feminino', 2020, 'algodão', 'estampada', 25.5, 10, 'bonitas roupas', 'gg');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (9, '1', 'camiseta manga longa', 'gola alta', 'masculino', 2021, 'algodão', 'vermelha', 29.9, 20, 'minha calça', 'p');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (10, '1', 'camiseta manga longa', 'gola alta', 'feminino', 2021, 'algodão', 'vermelha', 59.9, 20, 'roupa nova', 'p');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (11, '4', 'regata manga longa', 'regata', 'masculino', 2021, 'algodão', 'estampada', 59.2, 10, 'uahau roupa', 'p');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (12, '2', 'calça de moleton', 'esporte', 'masculino', 2020, 'moleton', 'azul', 29.9, 1, 'bonitas roupas', 'gg');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (13, '1', 'blusa manga longa com gola v', 'gola v', 'masculino', 2019, 'algodao', 'vermelha', 59.9, 10, 'roupa nova', 'g');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (14, '1', 'camiseta manga longa', 'esporte', 'feminino', 2020, 'poliester', 'estampado', 29.9, 1, 'bonitas roupas', 'gg');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (15, '12', 'shorts social', 'esporte fino', 'feminino', 2021, 'jeans', 'caqui', 59.9, 10, 'uahau roupa', 'g');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (16, '12', 'shorts social', 'esporte fino', 'masculino', 2021, 'jeans', 'branca', 10.0, 10, 'uahau roupa', 'gg');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (17, '1', 'larga na cintura e mangas', 'blusinha', 'feminino', 2021, 'seda', 'branca', 29.9, 5, 'a roupa nova do rei', 'm');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (18, '5', 'jaqueta jeans com pelo branco na gola', 'inverno', 'feminino', 2020, 'jeans', 'azul', 59.9, 10, 'bonitas roupas', 'pp');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (19, '5', 'blusao de moleton com bolsos', 'inverno', 'masculino', 2021, 'moleton', 'estampado', 59.9, 2, 'roupa nova', 'pp');
INSERT INTO produto (id, tipo_id, descricao, modelo, genero, ano_colecao, material, cor, preco, quantidade, marca_nome, tamanho_id) VALUES (20, '12', 'shorts jeans com cintura alta e barra desfiada', 'casual', 'masculino', 2020, 'jeans', 'preta', 29.9, 1, 'uahau roupa', 'gg');

-- Table: tamanho
CREATE TABLE tamanho (
	id VARCHAR(2) NOT NULL, 
	descricao VARCHAR(15) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO tamanho (id, descricao) VALUES ('gg', 'Extra Grande');
INSERT INTO tamanho (id, descricao) VALUES ('g', 'Grande');
INSERT INTO tamanho (id, descricao) VALUES ('m', 'Médio');
INSERT INTO tamanho (id, descricao) VALUES ('p', 'Pequeno');
INSERT INTO tamanho (id, descricao) VALUES ('pp', 'Muito Pequeno');

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
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (1, '2021-04-26 21:23:08.643036', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (2, '2021-04-26 21:23:46.295020', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (3, '2021-04-26 21:23:49.612319', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (4, '2021-04-26 21:23:58.611399', 1, 'M');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (5, '2021-04-26 21:44:30.715543', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (6, '2021-04-26 22:00:20.524614', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (7, '2021-04-26 22:01:51.540166', 1, 'Calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (8, '2021-04-26 22:03:13.094128', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (9, '2021-04-26 22:03:58.736665', 1, 'Calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (10, '2021-04-26 22:05:25.927203', 1, 'Calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (11, '2021-04-26 22:09:31.168489', 1, 'Calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (12, '2021-04-26 22:11:08.736158', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (13, '2021-04-26 22:13:12.621238', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (14, '2021-04-26 22:16:13.038739', 1, 'Calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (15, '2021-04-26 22:18:41.662929', 1, 'Calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (16, '2021-04-26 22:20:23.493816', 1, 'M');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (17, '2021-04-27 08:29:18.084847', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (18, '2021-04-27 08:30:49.397435', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (19, '2021-04-27 09:32:11.489862', 1, 'blusa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (20, '2021-04-27 09:35:08.489760', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (21, '2021-04-27 09:35:28.170668', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (22, '2021-04-27 09:35:53.870798', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (23, '2021-04-27 10:07:57.222044', 1, 'm');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (24, '2021-04-27 10:08:11.934860', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (25, '2021-04-27 10:08:58.668296', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (26, '2021-04-27 10:10:28.165694', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (27, '2021-04-27 10:10:53.461016', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (28, '2021-04-27 10:11:01.238363', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (29, '2021-04-27 10:11:05.183341', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (30, '2021-04-27 10:11:30.951449', 1, 'P');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (31, '2021-04-27 10:11:44.589939', 1, 'm');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (32, '2021-04-27 10:11:48.167336', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (33, '2021-04-27 10:11:51.422486', 1, 'p');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (34, '2021-04-27 10:11:54.910392', 1, 'pp');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (35, '2021-04-27 10:17:13.034094', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (36, '2021-04-27 10:17:15.806638', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (37, '2021-04-27 10:17:26.156613', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (38, '2021-04-27 10:26:52.293750', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (39, '2021-04-27 10:27:00.473052', 1, 'm');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (40, '2021-04-27 10:27:06.623106', 1, 'P');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (41, '2021-04-27 10:27:17.597114', 1, 'Pp');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (42, '2021-04-27 10:27:48.678478', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (43, '2021-04-27 10:27:50.591898', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (44, '2021-04-27 10:27:53.055136', 1, 'camisa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (45, '2021-04-27 10:27:59.480469', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (46, '2021-04-27 10:28:25.197480', 1, 'CALÇA');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (47, '2021-04-27 10:28:29.872140', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (48, '2021-04-27 10:28:31.337455', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (49, '2021-04-27 10:31:22.353934', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (50, '2021-04-27 10:34:42.009689', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (51, '2021-04-27 10:37:08.502312', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (52, '2021-04-27 10:39:56.257523', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (53, '2021-04-27 10:40:15.610558', 1, 'G');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (54, '2021-04-27 12:37:36.223280', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (55, '2021-04-27 12:46:40.462521', 1, 'blusa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (56, '2021-04-27 12:46:45.648299', 1, 'blusa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (57, '2021-04-27 12:46:51.679294', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (58, '2021-04-27 12:46:53.706466', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (59, '2021-04-27 12:47:49.741709', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (60, '2021-04-27 12:47:59.810873', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (61, '2021-04-27 12:48:41.209495', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (62, '2021-04-27 12:48:54.117679', 1, 'blusa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (63, '2021-04-27 13:20:52.006868', 1, 'moleton');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (64, '2021-04-27 13:22:12.241822', 1, 'moleton');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (65, '2021-04-27 13:22:25.496668', 1, 'Roupa Nova');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (66, '2021-04-27 13:22:39.655487', 1, 'Roupa Nova do Rei');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (67, '2021-04-27 13:22:48.474284', 1, 'A Roupa Nova do Rei');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (68, '2021-04-27 13:23:07.710121', 1, 'A Roupa Nova do Rei');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (69, '2021-04-27 13:24:52.419951', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (70, '2021-04-27 13:24:57.366773', 1, 'p');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (71, '2021-04-27 13:25:02.569650', 1, 'pp');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (72, '2021-04-27 13:25:10.216038', 1, 'blusa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (73, '2021-04-27 13:26:03.968412', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (74, '2021-04-27 13:26:12.081932', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (75, '2021-04-27 13:26:22.800978', 1, 'moleton');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (76, '2021-04-27 13:26:42.881134', 1, 'roupa nova');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (77, '2021-04-27 13:43:08.737776', 1, 2020);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (78, '2021-04-27 13:54:58.330396', 1, 2021);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (79, '2021-04-27 13:55:07.945540', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (80, '2021-04-27 13:55:26.130160', 1, 'p');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (81, '2021-04-27 13:55:35.142929', 1, 'pp');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (82, '2021-04-27 13:55:39.039138', 1, 'm');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (83, '2021-04-27 14:46:57.512284', 1, 'cal');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (84, '2021-04-27 14:47:06.897345', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (85, '2021-04-27 14:48:23.997846', 1, 'cal');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (86, '2021-04-27 14:48:41.194483', 1, 'calça de');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (87, '2021-04-27 14:51:47.984151', 1, 'calça de mo');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (88, '2021-04-27 17:53:17.472119', 1, 'Roupa Nova');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (89, '2021-04-27 17:53:56.764197', 1, 'oupa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (90, '2021-04-27 17:54:07.218435', 1, 'roupa nova do ');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (91, '2021-04-27 17:54:16.068941', 1, 'roupa nova');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (92, '2021-04-27 17:55:18.178849', 1, 'roupa nova');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (93, '2021-04-27 18:03:03.627673', 1, 4);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (94, '2021-04-27 18:04:21.436033', 1, 4);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (95, '2021-04-27 18:05:33.208233', 1, 4);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (96, '2021-04-27 18:06:10.657517', 1, 'esport');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (97, '2021-04-27 18:06:54.425704', 1, 'shorts, blusa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (98, '2021-04-27 20:30:33.424443', 1, 1);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (99, '2021-04-27 20:30:39.733454', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (100, '2021-04-27 20:30:53.784573', 1, 'baixa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (101, '2021-04-27 20:31:06.236467', 1, 'roupa nova');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (102, '2021-04-27 20:34:30.146671', 1, 'calça, 2020, gg');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (103, '2021-04-27 20:41:44.376819', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (104, '2021-04-27 21:52:05.304174', 1, 'regata');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (105, '2021-04-27 21:52:12.043360', 1, 'camiseta');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (106, '2021-04-27 21:53:09.741853', 1, 'roupa nova');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (107, '2021-04-27 21:53:16.761011', 1, 'ROUPA NOVA');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (108, '2021-04-27 21:56:18.776945', 1, 'CALÇA DE MOLETON');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (109, '2021-04-28 10:14:19.867915', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (110, '2021-04-28 10:14:27.541196', 1, 'p');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (111, '2021-04-28 10:14:57.145205', 1, 'medio');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (112, '2021-04-28 10:15:11.834292', 1, 'g');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (113, '2021-04-28 10:15:45.445345', 1, 'moleton');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (114, '2021-04-28 10:15:51.314921', 1, 20);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (115, '2021-04-28 10:15:54.698189', 1, 2020);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (116, '2021-04-28 10:15:58.407288', 1, 2021);
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (117, '2021-04-28 10:16:11.202390', 1, 'calca');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (118, '2021-04-28 10:16:21.783284', 1, 'calça, tamanho p');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (119, '2021-04-28 10:16:52.126890', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (120, '2021-04-30 19:54:40.677082', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (121, '2021-04-30 19:54:57.831101', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (122, '2021-04-30 19:55:11.877912', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (123, '2021-04-30 19:55:28.077299', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (124, '2021-04-30 19:55:43.444288', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (125, '2021-04-30 19:55:56.586184', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (126, '2021-04-30 19:56:20.840056', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (127, '2021-04-30 19:56:51.628292', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (128, '2021-04-30 19:57:54.584176', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (129, '2021-04-30 20:00:22.016039', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (130, '2021-04-30 20:00:25.436310', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (131, '2021-04-30 20:01:18.431311', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (132, '2021-04-30 20:52:31.559293', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (133, '2021-04-30 20:52:40.055345', 1, 'nova roupa');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (134, '2021-04-30 20:52:47.945371', 1, 'cintura');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (135, '2021-04-30 20:53:01.619194', 1, 'gola');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (136, '2021-04-30 20:53:11.606556', 1, 'esporte');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (137, '2021-04-30 22:51:25.870325', 1, 'esporte');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (138, '2021-04-30 22:52:38.256123', 1, 'calça');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (139, '2021-04-30 22:52:46.103987', 1, 'esporte');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (140, '2021-04-30 22:52:50.734999', 1, 'Esporte');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (141, '2021-04-30 22:52:51.911925', 1, 'Esporte');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (142, '2021-04-30 22:53:02.916983', 1, 'Espor');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (143, '2021-04-30 22:55:03.275598', 1, 'roupa no');
INSERT INTO transacao (id, data, user_id, produto_id) VALUES (144, '2021-04-30 22:56:26.152599', 1, 'esporte');

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
