#!/usr/bin/env python3
import cgi	# handling of user input in CGI scripts	
import cgitb	# displays nice tracebacks when errors occurs

import backend

cgitb.enable()

form = cgi.FieldStorage()

class Command:
	def __init__(self, cmd, params):
		self.cmd = cmd

		if params is None:
			params = ""

		self.params = params

	def __repr__(self):
		return self.cmd + ": " + self.params


def getCommands(form, id):
	cmds = form.getlist(id)
	return [ Command(cmd, form.getvalue(id + "_" + cmd)) for cmd in cmds ]


machine_ids = [ "maq" + str(i) for i in range(1, 4) ]
commands = {}
for id in machine_ids:
	commands[id] = getCommands(form, id)

response = backend.process(commands)

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print(commands)
print("</br>")
print(response)
