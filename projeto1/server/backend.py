import socket
import logging


def get_machine(maq_id):
	#TODO add config file to describe port number, and hostname
	ports = { 'maq1': 5000, 'maq2': 5001, 'maq3': 5002 }
	return ('localhost', ports[maq_id]) 


def send_command(maq, cmd):
	skt = socket.socket()
	skt.connect(get_machine(maq))

	logging.info("sending " + str(cmd) + " to " + str(get_machine(maq)))
	skt.send(cmd.cmd.encode())
	return skt.recv(1024).decode()


def process(maqs_cmds):
	st = ""
	response = {}	
	logging.debug("received " + str(maqs_cmds) + " to process")
	for maq, cmds in maqs_cmds.items():
		response[maq] = {}
		
		for cmd in cmds:
			response[maq][cmd] = send_command(maq, cmd)
	
	return response
