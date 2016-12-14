import socket
import logging
import sys

import protocol

def get_machine(maq_id):
	#TODO add config file to describe port number, and hostname
	ports = { 'maq1': 5000, 'maq2': 5001, 'maq3': 5002 }
	return ('localhost', ports[maq_id]) 


def send_command(maq, cmd):
	with socket.socket() as skt:
		skt.settimeout(3)

		try:
			skt.connect(get_machine(maq))
			msg = cmd.cmd + " " + cmd.params

			logging.debug("sending " + msg + " to " + str(get_machine(maq)))
			logging.debug("calling encode")

			encoded_msg = protocol.encode_request(cmd.cmd, cmd.params, None, None)
			#encoded_msg = msg.encode()

			logging.debug("sending encoded msg: " + str(encoded_msg) + str(type(encoded_msg)))

			skt.send(encoded_msg)

			logging.debug("sent")
			return skt.recv(1024).decode()
		except socket.timeout as exp:
			logging.debug("connection timed out")
			return "timeout"
		except:
			e = sys.exc_info()[0]
			logging.debug("could not connect to " + str(get_machine(maq)) + str(e))
			return "could not connect: %s" % str(e)


def process(maqs_cmds):
	st = ""
	response = {}	
	logging.debug("received " + str(maqs_cmds) + " to process")
	for maq, cmds in maqs_cmds.items():
		response[maq] = {}
		
		for cmd in cmds:
			response[maq][cmd] = send_command(maq, cmd)
			logging.debug(str(maq) + ", " + str(cmd) + ": " + str(response[maq][cmd]))
	
	logging.debug("returning response " + str(response))	
	return response
