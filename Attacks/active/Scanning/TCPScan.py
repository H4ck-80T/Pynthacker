import socket
import sys

addr=gethostbyname(sys.argv[1])
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

for i in range(0,65535):
	err=sock.connect_ex((addr,i))
	if err == 0:
		print "TCP port " + str(i) + " open"
		sock.close()
		sock = socket.socket(socket.AF_INET,sock.SOCK_STREAM)
