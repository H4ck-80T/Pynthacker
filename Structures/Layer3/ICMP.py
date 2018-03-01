'''
Build an ICMP packet from source. No defaults are assumed, the user is expected to carefully fill the fields.
Improper fields may cause unexplained behaviour.
'''

from struct import pack

class ICMP():
    'A class to represent and build the structure of an ICMP packet to be injected across the network'
    def __init__(self,type,code,id,seq):
        self.type=type
        self.code=code
        self.checksum=0
        self.ICMP_ID=id
        self.seq=seq
    def Packet(self):
        return pack('!BBHHH',self.type,self.code,self.checksum,self.ICMP_ID,self.seq)
