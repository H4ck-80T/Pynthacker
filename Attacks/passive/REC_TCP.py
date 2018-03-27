import sys
from pcap import *
from socket import *

'''
Receives the captured data from the control station and writes it inot a pcap file. Packets are received as TCP packets to ensure reliability.
'''

#TCP Receiving socket
sock=socket(AF_INET,SOCK_STREAM)
sock.bind(('',12345))
sock.listen(1)
rsock,r_addr=sock.accept()

#Logs the data by opening a PCAP file. Any existing file with the same name will be overwritten, so be careful!!
#Writes the PCAP file structure first, then appends packets inside the while loop that follows.
#Checks for the link layer header type for packets being captured
flag = int(rsock.recv(2))
print flag
if flag:
    pcap_global_header = pcap_global_header.replace('XX XX XX XX', '7F 00 00 00')
else:
    pcap_global_header = pcap_global_header.replace('XX XX XX XX', '01 00 00 00')
print pcap_global_header
h_file = open(sys.argv[1], 'wb')
writeBytes(pcap_global_header, h_file)

while 1:
    buf=rsock.recv(65536)
    if buf:
        writePCAP(buf,h_file)
        print buf

rsock.close()
sock.close()
