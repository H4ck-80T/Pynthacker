'''
Forge an ARP Packet. The argument list must be the same as the fields would appear in the packet. 
Since ARP deals with a wide variety of hardware and protocol types, NO defaults are assumed.
All arguments must be provided with proper care to avoid any undesirable behaviour.
'''

from socket import inet_aton,htons
from struct import pack


def make(base):
    base=base.split(':')
    d=''
    for item in base:
        d+=chr(int(item,16))
    return d


class ARP():
    def __init__(self,hrd,pro,op,sha,spa,tha,tpa):
        self.HRD=hrd
        self.PRO=(pro)
        if hrd == 1 or hrd == 6:
            self.HLN=0x06
        if pro == 0x0800:
            self.PLN=4
        self.OP=op
        self.SHA=make(sha)
        self.SPA=inet_aton(spa)
        self.THA=make(tha)
        self.TPA=inet_aton(tpa)
    def Packet(self):
        return pack('!HHBBH6s4s6s4s',self.HRD,self.PRO,self.HLN,self.PLN,self.OP,self.SHA,self.SPA,self.THA,self.TPA)





