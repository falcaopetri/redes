#!/usr/bin/env python3
import argparse
import socket
import threading
import logging
import subprocess
import protocol
import sys

class Command():
	def validate(cmd):
		'''
		A daemon deve fazer a checagem prévia destas opções antes de
		executá-las, garantidon que parâmetros maliciosos como 
		"|", ";" e ">" não sejam executados
		'''
		import re
		logging.debug("re")
		if re.search(r"[|;>]", cmd) is not None:
			logging.debug("re failed")
			return False
		logging.debug("re suc")
		
		return True


	def execute(cmd):
		# Shell True é necessário considerando que cmeh uma string unica
		# e não uma lista d eparametros
		try:
			process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
			logging.debug("subprocess.run(%s)" % cmd)
		except:
			e = sys.exc_info()[0]
			stdout = 'failed to execute process %s' % e
		else:
			stdout = process.stdout

		return str(stdout)


	def try_to_execute(data):
		logging.debug("try_to_execute " + str(data))
		if not Command.validate(data):
			logging.debug("cmd " + data + " failed validation")
			return None
		
		logging.debug("executing " + data)
		stdout = Command.execute(data)
		logging.debug("stdout " + stdout)
		return stdout


class ThreadedSocket:
	"""
	Referência: stackoverflow.com/a/23828265
	"""
	
	def __init__(self, args):
		# TODO remover hardcoded hostname
		self.hostname = "localhost"
		self.port = args.port

		self.skt = socket.socket()
		self.skt.bind( (self.hostname, self.port) )
		
		logging.debug("inited")


	def listenClient(conn, addr):
		conn.settimeout(2)
		while True:
			try:
				encoded_data = conn.recv(1024)
				logging.debug("received " + str(encoded_data))
				if not encoded_data:
					logging.debug("data is None?!")
					conn.close()
					break
					#raise error("Client disconnected")

				logging.debug("decoding")
				decoded_data = protocol.decode(encoded_data) 
				logging.debug("decoded data: " + str(decoded_data))
				stdout = Command.try_to_execute(decoded_data)
				# TODO passar src e dest IP's 
				response = protocol.encode_response("", stdout, None, None)
				logging.debug("encoded response: " + str(response))

				logging.debug("sending " + str(response))
				conn.send(response)
				logging.debug("sent and closed connection to " + str(addr))
				conn.close()
				break
			except:
				#conn.send("ops".encode())
				conn.close()
				break


	def listen(self):
		self.skt.listen()

		while True:
			conn, addr = self.skt.accept()
			conn.settimeout(3)
			threading.Thread(target=ThreadedSocket.listenClient, args=(conn, addr)).start()
			
		self.skt.close()

	

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("port", help="port on which to run the daemon", type=int)

	args = parser.parse_args()

	logging.basicConfig(filename='/tmp/daemon-' + str(args.port), level=logging.DEBUG)

	ThreadedSocket(args).listen()
