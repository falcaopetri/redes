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
			logging.debug("received encoded: %s" % encoded_response)
			decoded_response = protocol.decode(encoded_response)
			logging.debug("received decoded: %s" % str(decoded_response))

			return decoded_response
		except socket.timeout as exp:
			logging.debug("connection timed out")
			return ("", "timeout")
		except AssertionError as err:
			logging.debug("failed checksum while decoding response")
			# TODO improve ETRYAGAIN return
			return ("ETRYAGAIN", "failed checksum while decoding response")
		except:
			e = sys.exc_info()[0]
			logging.debug("could not connect to %s %s" % (str(get_machine(maq)), e))
			return ("", "could not connect: %s" % str(e))


def process(maqs_cmds):
	st = ""
	response = {}	
	logging.debug("received " + str(maqs_cmds) + " to process")
	for maq, cmds in maqs_cmds.items():
		response[maq] = {}
		
		for cmd in cmds:
			tries = 0
			r = send_command(maq, cmd)
			response[maq][cmd] = "Try 1: "
			
			while tries < 3 and r[0] == "ETRYAGAIN":
				response[maq][cmd] += "%s\n\n" % r[1]
				r = send_command(maq, cmd)
				tries += 1
				response[maq][cmd] += "Try %d: " % (tries+1)
		
			response[maq][cmd] += "\n%s" % r[1] 
			logging.debug("%s, %s: %s" % (maq, cmd, response[maq][cmd]))
	
	logging.debug("returning response " + str(response))	
	return response
