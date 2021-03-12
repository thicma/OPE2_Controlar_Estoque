import mysql.connector

dao = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin',
    database = 'estoque'
)

cursor = dao.cursor()

cria_tabelas = '''
                CREATE TABLE IF NOT EXISTS TIPO_AUTORIZACAO(
                    ID_AUTORIZACAO INT(1) NOT NULL PRIMARY KEY,
                    DESCRICAO_AUTORIZACAO VARCHAR(10),
                    PODE_ALTERAR_PRODUTO BIT(1),
                    PODE_CADASTRAR_PRODUTO BIT(1),
                    PODE_CONSULTAR_PRODUTO BIT(1),
                    PODE_EXCLUIR_PRODUTO BIT(1),
                    PODE_SOLICITAR_PRODUTO BIT(1)
                    );
                CREATE TABLE IF NOT EXISTS USUARIO(
                    MATRICULA INT NOT NULL PRIMARY KEY,
                    SENHA VARCHAR(20),
                    NOME VARCHAR(100),
                    AUTORIZACAO INT(1)
                    );
                CREATE TABLE IF NOT EXISTS FORNECEDOR(
                    ID_FORNECEDOR INT NOT NULL PRIMARY KEY,
                    NOME VARCHAR(50),
                    EMAIL VARCHAR(100),
                    TELEFONE VARCHAR(20),
                    CNPJ VARCHAR(20));
                CREATE TABLE IF NOT EXISTS TIPO_PRODUTO(
                    ID_TIPO_PRODUTO INT NOT NULL PRIMARY KEY,
                    DESCRICAO VARCHAR(50),
                    MODELO VARCHAR(20)
                    );
                CREATE TABLE IF NOT EXISTS TIPO_MATERIAL(
                    ID_TIPO_MATERIAL INT NOT NULL PRIMARY KEY,
                    DESCRICAO_MATERIAL VARCHAR(50)
                    );
                CREATE TABLE IF NOT EXISTS TAMANHO_PRODUTO(
                    ID_TAMANHO_PRODUTO VARCHAR(2) PRIMARY KEY,
                    DESCRICAO_TAMANHO VARCHAR(15)
                    );
                CREATE TABLE IF NOT EXISTS MARCA(
                    NOME_MARCA VARCHAR(20) NOT NULL PRIMARY KEY,
                    FORNECEDOR INT,
                    FOREIGN KEY (FORNECEDOR) REFERENCES fornecedor (ID_FORNECEDOR));
                CREATE TABLE IF NOT EXISTS PRODUTO(
                    ID_PRODUTO VARCHAR(20) NOT NULL PRIMARY KEY,
                    COR VARCHAR(20),
                    PRECO FLOAT,
                    QUANTIDADE INT,
                    TIPO_PRODUTO INT,
                    TAMANHO VARCHAR(2),
                    MARCA VARCHAR(20),
                    ANO_MODELO YEAR(4),
                    TIPO_MATERIAL INT,
                    FOREIGN KEY (TIPO_PRODUTO) REFERENCES TIPO_PRODUTO (ID_TIPO_PRODUTO),
                    FOREIGN KEY (TAMANHO) REFERENCES TAMANHO_PRODUTO (ID_TAMANHO_PRODUTO),
                    FOREIGN KEY (MARCA) REFERENCES MARCA (NOME_MARCA),
                    FOREIGN KEY (TIPO_MATERIAL) REFERENCES TIPO_MATERIAL (ID_TIPO_MATERIAL)
                    );
                CREATE TABLE IF NOT EXISTS TRANSACAO(
                    ID_TRANSACAO INT NOT NULL AUTO_INCREMENT,
                    DATA_TRANSACAO TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
                    USUARIO INT,
                    ID_PRODUTO VARCHAR(20),
                    TIPO_AUTORIZACAO INT(1),
                    PRIMARY KEY (ID_TRANSACAO),
                    FOREIGN KEY (USUARIO) REFERENCES USUARIO (MATRICULA),
                    FOREIGN KEY (ID_PRODUTO) REFERENCES PRODUTO (ID_PRODUTO),
                    FOREIGN KEY (TIPO_AUTORIZACAO) REFERENCES TIPO_AUTORIZACAO (ID_AUTORIZACAO));
                     '''
cursor.execute(cria_tabelas)
