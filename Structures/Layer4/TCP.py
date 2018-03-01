from struct import pack
from socket import htons

class TCP():
    window=htons(5840)
    checksum=0
    URG_P=0
    Data=''
    def __init__(self,s_port,d_port,seq,ackno,size_flags=0x5000):
        self.SRC_P=s_port
        self.DST_P=d_port
        self.SEQ_NO=seq
        self.ACK_NO=ackno
        self.size_flags=size_flags
    def Flags(self,Nonce,ECN,ECN_Echo,URG,ACK,PSH,RST,SYN,FIN):
        if Nonce:
            self.size_flags=self.size_flags|0x0100
        if ECN:
            self.size_flags=self.size_flags|0x0080
        if ECN_Echo:
            self.size_flags=self.size_flags|0x0040
        if URG:
            self.size_flags=self.size_flags|0x0020
        if ACK:
            self.size_flags=self.size_flags|0x0010
        if PSH:
            self.size_flags=self.size_flags|0x0008
        if RST:
            self.size_flags=self.size_flags|0x0004
        if SYN:
            self.size_flags=self.size_flags|0x0002
        if FIN:
            self.size_flags=self.size_flags|0x0001
    def Set(self,payload):
        self.Data=payload
    def Options(self):
        pass
    def Packet(self):
        if self.size_flags < 0x6000:
            return pack('!HHLLHHHH',self.SRC_P,self.DST_P,self.SEQ_NO,self.ACK_NO,self.size_flags,self.window,self.checksum,self.URG_P) + self.Data
        else:
            #return pack('!HHLLHHHH',self.SRC_P,self.DST_P,self.SEQ_NO,self.ACK_NO,self.size_flags,self.window,self.checksum,self.URG_P) + self.Data
            pass  

