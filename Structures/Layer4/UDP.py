from struct import pack

class UDP():
    checksum=0
    UDP_len=0x08
    def __init__(self,s_port,d_port):
        self.SRC_P=s_port
        self.DST_P=d_port
    def Set(self,payload):
        self.Data=payload
        self.UDP_len+=len(payload)
    def Packet(self):
        if self.UDP_len == 0x08:
            return pack('!HHHH',self.SRC_P,self.DST_P,self.UDP_len,self.checksum)
        else:
            return pack('!HHHH',self.SRC_P,self.DST_P,self.UDP_len,self.checksum) + self.Data