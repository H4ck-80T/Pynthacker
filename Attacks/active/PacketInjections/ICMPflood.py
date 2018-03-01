'''
Script to send custom ICMP packets.
This script allows the user full control over the entire processing spectrum. The user has liberty to control every header right from the Link Layer headers.
The user is given an option to customise headers if required.

The inputs are required to be entered as and when prompted.

Notes:
-> Reuires root/Admin
-> Not advisable when knowledge of kernel routing tables is unknown

Example Usage:
root@localhost:~#python ICMP_Flood.py
'''

import sys, socket, time
sys.path.append( <absolute path to /Structures> )
from Layer2 import EthernetFrame
from Layer3.ICMP import *
from Layer3.IPv4 import *

#Prompt the user to enter the ICMP field headers
print "Enter the ICMP fields in their proper order:\n"
ICMP_CODE = input('icmp code:\n')
ICMP_TYPE = input('icmp type:\n')
ICMP_ID = input('icmp id:\n')
ICMP_SEQ = input('icmp seq no:\n')
#Now prepare the ICMP packet
icmp = ICMP(ICMP_CODE, ICMP_TYPE, ICMP_ID, ICMP_SEQ).Packet()
choice = raw_input("Do you want to customise the IP header?(Y/N)\n")
if choice == 'N':
    print "Enter the local and remote IP addresses:\n"
    L_ADDR = raw_input('local IP:\n')
    R_ADDR = raw_input('remote IP:\n')

    #Creates a raw socket of address family AF_INET and protocol definition ICMP
    sock=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
    sock.bind((L_ADDR,0))

    #Portnumber does not matter in ICMP
    while 1:
        sock.sendto(icmp,(R_ADDR,0))
        time.sleep(2)
elif choice == 'Y':
    #Prompt IP headers
    print "Enter the IP header fields in their order:\n"
    IPID = input('IPID:\n')
    FRG = input('Fragment?(0/1)\n')
    TTL = input('Time To Live:\n')
    S_ADDR = raw_input('Source IP:\n')
    D_ADDR = raw_input('Destination IP:\n')
    #Forge the IP packet
    ip = IPv4(IPID, FRG, TTL, 0x01, S_ADDR, D_ADDR).Packet()
    choice = raw_input("Do you want to customise the Link Layer (Ethernet) header?(Y/N)\n")
    if choice == 'N':
        sock=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)
        IFACE = raw_input('Enter the IP address of interface to bind to:\n')
        sock.bind((IFACE,0))
        while 1:
            sock.sendto(ip+icmp,(raw_input('Enter destination'),0))
            time.sleep(2)
    elif choice == 'Y':
        #Prompt Ethernet headers
        S_MAC = raw_input('Sorce MAC:\n')
        D_MAC = raw_input('Destination MAC:\n')
        Eth = EthernetFrame(S_MAC,D_MAC,0x0800).Frame()
        #Packet level raw socket needed
        sock=socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x0003))
        sock.bind((raw_input('Enter the interface:\n'),0))
        while 1:
            sock.send(Eth + ip + icmp)
            time.sleep(2)
