#!/usr/bin/env python3
import socket
import time, sys
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

host = 'www.google.com'
port = 80
buffer_size = 4096

#get host information
def get_remote_ip(host):
	print(f'Getting IP for {host}')
	try:
		remote_ip = socket.gethostbyname( host )
	except socket.gaierror:
		print ('Hostname could not be resolved. Exiting')
		sys.exit()

	print (f'Ip address of {host} is {remote_ip}')
	return remote_ip


def handle_request(conn, addr, proxy_end):

	# send data 
	send_full_data = conn.recv(BUFFER_SIZE)
	time.sleep(0.5)


	print(f"sending recieved data {send_full_data} to google")
	proxy_end.sendall(send_full_data)

	# rshut down
	proxy_end.shutdown(socket.SHUT_WR)



	# #recieve data, wait a bit, then send it back
	# full_data = proxy_end.recv(BUFFER_SIZE)

	#continue accepting data until no more left
	full_data = b""
	while True:
		data = proxy_end.recv(buffer_size)
		if not data:
			break
		full_data += data

	# print(full_data)


	conn.sendall(full_data)
	conn.shutdown(socket.SHUT_WR)
	conn.close()
	

def main():
	# question 6 Address


	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
		print("Staring proxy server")
		# allow reused adderss, bind and set to listening mode
		# connect to proxy_client
		proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		proxy_start.bind((HOST, PORT))
		proxy_start.listen(1)
		#continuously listen for connections
		while True:
			conn, addr = proxy_start.accept()
			print("Connected by", addr)
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
				print("Connecting to Google")
				remote_ip = get_remote_ip(host)

				# connect proxy_end, connect to google
				proxy_end.connect((remote_ip, port))

				p = Process(target = handle_request, args= (conn, addr, proxy_end))
				p.dameon = True
				p.start()
				print("Staring process", p)

		proxy_start.close()

if __name__ == "__main__":
	main()
