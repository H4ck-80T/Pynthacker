from socket import *
import sys

addr=gethostbyname(sys.argv[1])
sock = socket(AF_INET,SOCK_STREAM)

for i in range(0,65535):
	err=sock.connect_ex((addr,i))
	if err == 0:
		print "TCP port " + str(i) + " open"
