'''
Script to sniff packets from the surrounding environment and send them across the network for analysis.
Uses two interfaces; one to sniff and one to send the sniffed data across.

Parameters:
The interface to sniff over
If the sniffing is done in monitor mode (RFMON) then 1 is expected as the second argument; or else the second argument is 0
The destination to send the sniffed data

Notes:
-> Requires Root/Admin
-> The user manually needs to enbale the mode on the sniffing interface. (Monitor/Promiscous/Managed) 
Example usage:
root@localhost:~#sudo python SNR_TCP.py ath1 0 10.10.10.10 
'''

import socket,sys

#Create the sniffer
sniffer = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x0003))
sniffer.bind((sys.argv[1],(0x0003)))

#create the sender
sender =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sender.connect((sys.argv[3],12345))
sender.send(sys.argv[2]) 

while 1:
    #sniff data
    buffer = sniffer.recvfrom(65536)
    if buffer:
        #immediately send data to station
        print buffer
        sender.send(buffer[0])