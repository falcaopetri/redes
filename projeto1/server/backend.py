import socket
import logging
import sys

import protocol
import util

config = util.get_config()

def get_machine(maq_id):
	if maq_id not in config['daemons']:
		raise NameError("%s not defined in config file" % maq_id)

	return tuple(config['daemons'][maq_id])


def send_command(maq, cmd):
	with socket.socket() as skt:
		skt.settimeout(3)

		try:
			skt.connect(get_machine(maq))
			msg = cmd.cmd + " " + cmd.params

			logging.debug("sending " + msg + " to " + str(get_machine(maq)))
			logging.debug("calling encode")

			encoded_request = protocol.encode_request(cmd.cmd, cmd.params, None, None)

			logging.debug("sending encoded msg: " + str(encoded_request) + str(type(encoded_request)))

			skt.send(encoded_request)

			logging.debug("sent")
			encoded_response = skt.recv(1024)
			logging.debug("received encoded: ", encoded_response)
			decoded_response = protocol.decode(encoded_response)
			logging.debug("received decoded: ", decoded_response)

			return decoded_response
		except socket.timeout as exp:
			logging.debug("connection timed out")
			return "timeout"
		except:
			e = sys.exc_info()[0]
			logging.debug("could not connect to %s %s" % (str(get_machine(maq)), e))
			return "could not connect: %s" % str(e)


def process(maqs_cmds):
	st = ""
	response = {}	
	logging.debug("received " + str(maqs_cmds) + " to process")
	for maq, cmds in maqs_cmds.items():
		response[maq] = {}
		
		for cmd in cmds:
			response[maq][cmd] = send_command(maq, cmd)[1]
			logging.debug("%s, %s: %s" % (maq, cmd, response[maq][cmd]))
	
	logging.debug("returning response " + str(response))	
	return response
