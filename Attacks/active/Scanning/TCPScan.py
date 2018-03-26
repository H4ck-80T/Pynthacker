import socket
import sys

addr=socket.gethostbyname(sys.argv[1])

for i in range(0,65535):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(2)
	err=sock.connect_ex((addr,i))
	if err == 0:
		print "TCP port " + str(i) + " open"
		sock.close()
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	

		
