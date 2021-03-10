import re
def sanitizar_insert(coluna,valor):
	ret=True
	if (coluna=='MATRICULA' or coluna=='AUTORIZACAO' or coluna=='CODIGO_TRANSACAO' or coluna=='NIVEL_TRANSACAO' or coluna=='COD_FORNECEDOR' or coluna=='ID_TIPO' or coluna=='FORNECEDOR'or coluna=='QUANTIDADE' or coluna=='TIPO' or coluna=='USUARIO' or coluna== 'TIPO_TRANSACAO'):
		try:
			int(valor)
		except:
			print ("Essa coluna deve conter apenas digitos!")
			ret=False
	elif (coluna=='SENHA'):
		chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*(){}[]<>?-+="
		if (len(valor)>20):
			print ("Input muito longo")
			ret=False
		for i in valor:
			if (i not in chars):
				print ("caractere invalido!")
				ret=False
				break
	elif (coluna=='NOME'):
		chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ "
		if (len(valor)>100):
			print("Input muito longo")
			ret=False
		for i in valor:
			if (i not in chars):
				print ("caractere invalido!")
				ret=False
				break
	elif (coluna=='CARGO'):
		chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
		if (len(valor)>20):
			print ("Input muito longo")
			ret=False
		for i in valor:
			if (i not in chars):
				print("caractere invalido!")
				ret=False
				break
	elif (coluna=='NOME_TRANSACAO'):
		chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ "
		if (len(valor)>10):
			print("Input muito longo")
			ret=False
		for i in valor:
			if (i not in chars):
				print("caractere invalido!")
				ret=False
				break
	elif (coluna=='EMAIL'):
		if (len(valor)>100):
			print ("Input muito longo!")
			ret=False
		if (not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$",valor)):
			ret=False
	elif (coluna=='TELEFONE'):
		if (len(valor)>20):
			print("Input muito longo!")
			ret=False
		if (not re.match("^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$",valor)):
			ret=False
	elif (coluna=='CNPJ'):
		if (len(valor)>20):
			print ("Input muito longo!")
			ret=False
		if (not re.match("^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$",valor)):
			ret=False
	return ret



