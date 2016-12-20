#!/usr/bin/env python3
import cgi	# handling of user input in CGI scripts	
import cgitb	# displays nice tracebacks when errors occurs
import logging
import subprocess

import backend
import protocol
import util


config = util.get_config()

cgitb.enable()
logging.basicConfig(filename=config['logging']['server'], level=logging.DEBUG)

form = cgi.FieldStorage()

class Command:
	def __init__(self, cmd, params):
		self.cmd = str(cmd)

		if params is None:
			params = ""

		self.params = str(params)

	def __repr__(self):
		return self.cmd + " " + self.params

	def __lt__(self, other):
		# enables sorting on list of Commands
		# used to always display commands on the same order
		return str(self) < str(other)

def getCommands(form, id):
	cmds = form.getlist(id)
	return [ Command(cmd, form.getvalue(id + "_" + cmd)) for cmd in cmds ]


machine_ids = config['daemons'].keys()
commands = {}
for id in machine_ids:
	commands[id] = getCommands(form, id)


logging.debug('sending ' + str(commands) + ' to backend')
response = backend.process(commands)
logging.debug('received ' + str(response) + ' from backend')

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print("<body class=\"body_foreground body_background\" style=\"font-size: normal;\" >")

print("</br>")

def printDict(dictObj, indent):
	# source stackoverflow.com/a/3930913
	print('  '*indent + '<ul>\n')
	itr = dictObj if isinstance(dictObj, list) else dictObj.items()
	for k, v in itr:
		if isinstance(v, dict):
			print('  '*indent, '<li>', k, ':', '</li>')
			v = sorted(v.items(), key=operator.itemgetter(0))
			printDict(v, indent+1)
		else:
			print("<pre class=\"ansi2html-content\">")
			print(' '*indent, '<li>', k, ':', '</li>')
			stdout = subprocess.run("echo \"%s\" | ansi2html -i"  % v, stdout=subprocess.PIPE, shell=True).stdout
			stdout = stdout.decode()
			print(stdout)
			print("<pre>")
	print(' '*indent + '</ul>\n')

import operator
response = sorted(response.items(), key=operator.itemgetter(0))
printDict(response, 2)
print("</body>")

print("</html>")
logging.debug("end")
