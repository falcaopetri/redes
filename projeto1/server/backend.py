import socket
import logging

import protocol

def get_machine(maq_id):
	#TODO add config file to describe port number, and hostname
	ports = { 'maq1': 5000, 'maq2': 5001, 'maq3': 5002 }
	return ('localhost', ports[maq_id]) 


def send_command(maq, cmd):
	with socket.socket() as skt:
		skt.settimeout(3)

		skt.connect(get_machine(maq))
		try:
			msg = cmd.cmd + " " + cmd.params

			logging.debug("sending " + msg + " to " + str(get_machine(maq)))
			logging.debug("calling encode")

			encoded_msg = protocol.encode_request(cmd.cmd, cmd.params, None, None)
			# encoded_msg = msg.encode()

			logging.debug("sending encoded msg: " + str(encoded_msg) + str(type(encoded_msg)))

			skt.send(encoded_msg)

			logging.debug("sent")

			return skt.recv(1024).decode()
		except socket.timeout as exp:
			return "timeout"
		except:
			return "could not connect"


def process(maqs_cmds):
	st = ""
	response = {}	
	logging.debug("received " + str(maqs_cmds) + " to process")
	for maq, cmds in maqs_cmds.items():
		response[maq] = {}
		
		for cmd in cmds:
			response[maq][cmd] = send_command(maq, cmd)
	
	return response
