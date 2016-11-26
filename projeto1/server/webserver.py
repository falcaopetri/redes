#!/usr/bin/env python3
import cgi	# handling of user input in CGI scripts	
import cgitb	# displays nice tracebacks when errors occurs
import logging

import backend

cgitb.enable()
logging.basicConfig(filename='/home/aluno/redes/projeto1/server.log', level=logging.DEBUG)

form = cgi.FieldStorage()

class Command:
	def __init__(self, cmd, params):
		self.cmd = str(cmd)

		if params is None:
			params = ""

		self.params = params

	def __repr__(self):
		return self.cmd + ": " + self.params


def getCommands(form, id):
	cmds = form.getlist(id)
	return [ Command(cmd, form.getvalue(id + "_" + cmd)) for cmd in cmds ]


logging.debug('here')
machine_ids = [ "maq" + str(i) for i in range(1, 4) ]
commands = {}
for id in machine_ids:
	commands[id] = getCommands(form, id)


logging.debug('sending ' + str(commands) + ' to backend')
response = backend.process(commands)

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print(commands)
print("</br>")

def printDict(dictObj, indent):
	# source stackoverflow.com/a/3930913
	print('  '*indent + '<ul>\n')
	for k, v in dictObj.items():
		if isinstance(v, dict):
			print('  '*indent, '<li>', k, ':', '</li>')
			printDict(v, indent+1)
		else:
			print(' '*indent, '<li>', k, ':', v.replace('\\n', '</br>'), '</li>')
	print(' '*indent + '</ul>\n')

printDict(response, 2)
