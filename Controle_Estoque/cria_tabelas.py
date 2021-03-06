import mysql.connector

dao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin',
    database = 'estoque2'
)

cursor = dao.cursor()

cria_tabelas = '''
                CREATE TABLE IF NOT EXISTS USUARIO(
                    MATRICULA INT NOT NULL PRIMARY KEY,
                    SENHA VARCHAR(20),
                    NOME VARCHAR(100),
                    CARGO VARCHAR(20),
                    AUTORIZACAO INT(1)
                    )ENGINE=InnoDB;

                CREATE TABLE IF NOT EXISTS TIPO_TRANSACAO(
                    CODIGO_TRANSACAO INT(1) NOT NULL PRIMARY KEY,
                    NOME_TRANSACAO VARCHAR(10),
                    NIVEL_TRANSACAO INT(1));

                CREATE TABLE IF NOT EXISTS FORNECEDOR(
                    COD_FORNECEDOR INT NOT NULL PRIMARY KEY,
                    NOME VARCHAR(50),
                    EMAIL VARCHAR(100),
                    TELEFONE VARCHAR(20),
                    CNPJ VARCHAR(20));

                CREATE TABLE IF NOT EXISTS TIPO(
                    ID_TIPO INT NOT NULL PRIMARY KEY,
                    DESCRICAO VARCHAR(50),
                    MATERIAL VARCHAR(20),
                    MODELO VARCHAR(20),
                    ANO_COLECAO YEAR);

                CREATE TABLE IF NOT EXISTS TAMANHO(
                    ID_TAMANHO VARCHAR(2),
                    DESCRICAO_TAMANHO VARCHAR(15));

                CREATE TABLE IF NOT EXISTS MARCA(
                    NOME_MARCA VARCHAR(20) NOT NULL PRIMARY KEY,
                    FORNECEDOR INT,
                    FOREIGN KEY (FORNECEDOR) REFERENCES (COD_FORNECEDOR));

                CREATE TABLE IF NOT EXISTS PRODUTO(
                    CODIGO VARCHAR(20) NOT NULL PRIMARY KEY,
                    COR VARCHAR(20),
                    PRECO FLOAT,
                    QUANTIDADE INT,
                    TIPO INT,
                    TAMANHO VARCHAR(2),
                    MARCA VARCHAR(20),
                    FOREIGN KEY (TIPO) REFERENCES TIPO (ID_TIPO),
                    FOREIGN KEY (TAMANHO) REFERENCES TAMANHO (ID_TAMANHO),
                    FOREIGN KEY (MARCA) REFERENCES MARCA (NOME_MARCA));

                CREATE TABLE IF NOT EXISTS TRANSACAO(
                    ID_TRANSACAO INT NOT NULL AUTO_INCREMENT,
                    DATA_TRANSACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                    USUARIO INT,
                    COD_PRODUTO VARCHAR(20),
                    TIPO_TRANSACAO INT(1),
                    PRIMARY KEY (ID_TRANSACAO),
                    FOREIGN KEY (USUARIO) REFERENCES USUARIO (MATRICULA),
                    FOREIGN KEY (COD_PRODUTO) REFERENCES PRODUTO (CODIGO),
                    FOREIGN KEY (TIPO_TRANSACAO) REFERENCES TIPO_TRANSACAO (COD_TRANSACAO));
                     '''
cursor.execute(cria_tabelas)
