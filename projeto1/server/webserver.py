#!/usr/bin/env python3
import cgi	# handling of user input in CGI scripts	
import cgitb	# displays nice tracebacks when errors occurs
import logging
import subprocess

import backend
import protocol

cgitb.enable()
logging.basicConfig(filename='/tmp/server.log', level=logging.DEBUG)

form = cgi.FieldStorage()

class Command:
	def __init__(self, cmd, params):
		self.cmd = str(cmd)

		if params is None:
			params = ""

		self.params = str(params)

	def __repr__(self):
		return self.cmd + " " + self.params


def getCommands(form, id):
	cmds = form.getlist(id)
	return [ Command(cmd, form.getvalue(id + "_" + cmd)) for cmd in cmds ]


machine_ids = [ "maq" + str(i) for i in range(1, 4) ]
commands = {}
for id in machine_ids:
	commands[id] = getCommands(form, id)


logging.debug('sending ' + str(commands) + ' to backend')
response = backend.process(commands)
logging.debug('received ' + str(response) + ' from backend')

print("Content-Type: text/html;charset=utf-8\r\n\r\n")


print("<html>")
print("<head>")
stdout = subprocess.run("ansi2html -H", stdout=subprocess.PIPE, shell=True).stdout
print(stdout.decode())
#print("<\head>")
print("")


print("<body class=\"body_foreground body_background\" style=\"font-size: normal;\" >")
#print(commands)

print("</br>")

def printDict(dictObj, indent):
	# source stackoverflow.com/a/3930913
	print('  '*indent + '<ul>\n')
	for k, v in dictObj.items():
		if isinstance(v, dict):
			print('  '*indent, '<li>', k, ':', '</li>')
			printDict(v, indent+1)
		else:
			print("<pre class=\"ansi2html-content\">")
			#print(' '*indent, '<li>', k, ':', v.replace('\\n', '</br>'), '</li>')
			stdout = subprocess.run("echo \"%s\" | ansi2html"  % v, stdout=subprocess.PIPE, shell=True).stdout
			print(stdout.decode())
			print("<pre>")
	print(' '*indent + '</ul>\n')

printDict(response, 2)

print("</body>")

print("</html>")
logging.debug("end")
