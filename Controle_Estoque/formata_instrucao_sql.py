
def formatar_instrucao_sql(nome_tabela, nome_colunas):
    nome_tabela = nome_tabela
    nome_colunas = nome_colunas

    nome_colunas_sql = ''
    for apenas_nome_coluna in nome_colunas:
        if apenas_nome_coluna is not nome_colunas[-1]:
            nome_colunas_sql += apenas_nome_coluna + ', '
        else:    
            nome_colunas_sql += apenas_nome_coluna            
    quantidade_de_atributos = (','+ '%s')  * len(nome_colunas)
    quantidade_de_atributos = quantidade_de_atributos.replace(',','',1)

    instrucao_sql = f'''INSERT INTO {nome_tabela} ({nome_colunas_sql})
                    VALUES ({quantidade_de_atributos});'''

    return instrucao_sql