import os
import json

def get_config():
	'''
	Retorna um dicionário com as configurações carregadas do arquivo de configuração.
	O PATH desse arquivo está hardcoded dentro dessa função.
	O nome do arquivo também está hardcoded dentro dessa função.
	'''
	# TODO o path deveria estar hardcoded aqui?
	# TODO o nome do arquivo deveria estar hardcoded ou ser um argumento?
	os.chdir('/home/aluno/redes/projeto1')

	with open('config.json', 'r') as f:
        	config = json.load(f)

	return config
