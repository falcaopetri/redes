import os
import json

def get_config():
	os.chdir('/home/aluno/redes/projeto1')

	with open('config.json', 'r') as f:
        	config = json.load(f)

	return config
