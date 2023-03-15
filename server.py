import socket
import sys
from _thread import *
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.bind((IP_address, Port))

server.listen(100)

list_of_clients = []
msg ="Welcome to this chatroom!"
def clientthread(conn, addr):
	conn.send(msg.encode('utf-8'))

	while True:
			try:
				message = conn.recv(2048).decode()
				if message:
					print ("<" + addr[0] + "> " + message)
					message_to_send = "<" + addr[0] + "> " + message
					broadcast(message_to_send, conn)
					nmsg = input()
					print("<You>",nmsg)
					conn.send(nmsg.encode('utf-8'))
				else:
					remove(conn)

			except:
				continue
def broadcast(message, connection):
	for clients in list_of_clients:
		if clients!=connection:
			try:
				clients.send(message.encode('utf-8'))
			except:
				clients.close()

				remove(clients)
def remove(connection):
	if connection in list_of_clients:
		list_of_clients.remove(connection)

while True:
	conn, addr = server.accept()
	list_of_clients.append(conn)
	print (addr[0] + " connected")
	start_new_thread(clientthread,(conn,addr))	

conn.close()
server.close()
