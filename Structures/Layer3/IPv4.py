'''
Forge an IPv4 packet to be sent across the network. Fields except the addresses are expected as 8 bit words.
The user is expected to pre calculate the 8 bit words corresponding to various flags to avoid any unexpected behaviour.
Does not assume the presence of options field. Please use the provided Options() function to add options before building the packet.
'''


from struct import pack
from socket import inet_aton,htons,htonl

class IPv4():
    'Builds an IPv4 Packet'
    VIHL=0x45
    TOS=0x00  #Now known an Differentiated Services Code Point (DSCP)
    total_len=0
    checksum=0
    def __init__(self,id,df,ttl,proto,s_addr,d_addr):
        self.IPID=id
        if df:
            self.Flag_FragOffset=0x4000
        else:
            self.Flag_FragOffset=0x2000
        self.TTL=ttl
        self.proto=proto
        self.SRC_IP=inet_aton(s_addr)
        self.DST_IP=inet_aton(d_addr)
    def Change(self,id,frag):
        self.IPID=id
        self.Flag_FragOffset=self.Flag_FragOffset|frag
    def Packet(self):
        return pack('!BBHHHBBH4s4s',self.VIHL,self.TOS,self.total_len,self.IPID,self.Flag_FragOffset,self.TTL,self.proto,self.checksum,self.SRC_IP,self.DST_IP)
    def Options(self):
        pass