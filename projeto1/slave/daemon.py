#!/usr/bin/env python3
import argparse
import socket
import subprocess	

parser = argparse.ArgumentParser()
parser.add_argument("port", help="port on which to run the daemon", type=int)

args = parser.parse_args()


skt = socket.socket()
skt.bind( ("localhost", args.port) )

skt.listen(1)
while True:
	conn, addr = skt.accept()

	while True:
		data = conn.recv(1024).decode()

		if not data:
			break

		# TODO validate data (cmd)
		process = subprocess.run(data, stdout=subprocess.PIPE)
		stdout = str(process.stdout)

		conn.send(stdout.encode())

	conn.close()

