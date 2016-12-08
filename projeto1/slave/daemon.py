#!/usr/bin/env python3
import argparse
import socket
import threading
import logging
import subprocess
# import protocol
 
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
		# Shell True é necessário considerando que cmd é uma sng unica
		# e não uma lista de prâmetr
		process = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
		stdout = str(process.stdout)

		return stdout


	def try_to_execute(encoded_data):
		# decoded_data = protocol.decode(encoded_data)
		decoded_data = str(encoded_data)
		logging.debug("try_to_execute " + str(encoded_data))
		if not Command.validate(decoded_data):
			logging.debug("cmd " + decoded_data + " failed validation")
			return None
		
		logging.debug("executing " + decoded_data)
		stdout = Command.execute(decoded_data)
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
		while True:
			try:
				data = conn.recv(1024).decode()
				logging.debug("received " + str(data))
				if not data:
					logging.debug("data is None?!")
					raise error("Client disconnected")

				try:	
					response = Command.try_to_execute(data)
				
					logging.debug("sending " + str(response.encode()))
					conn.send(response.encode())
					logging.debug("sent and closed connection to " + str(addr))
				finally:
					conn.close()
					break
			except:
				conn.close()
				break


	def listen(self):
		self.skt.listen()

		while True:
			conn, addr = self.skt.accept()
			conn.settimeout(3)
			threading.Thread(target=ThreadedSocket.listenClient, args=(conn, addr)).start()

	

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("port", help="port on which to run the daemon", type=int)

	args = parser.parse_args()

	logging.basicConfig(filename='/tmp/daemon-' + str(args.port), level=logging.DEBUG)

	ThreadedSocket(args).listen()
