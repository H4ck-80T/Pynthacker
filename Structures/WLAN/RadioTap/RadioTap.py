from struct import pack
from socket import htons,htonl

class RadioTap():
    'Builds a standard Radio Tap header. Version is always 0 with a fixed padding. Variable fields are initiated via __init__(). Since packet crafting is to be done in a responsible manner, the crafter is expected to know the length and custom fields before hand' 
    it_version=0x00
    it_pad=0x00
    def __init__(self,len=0x000b,bitmap=0x00028000,r=0x00,t=0x00,a=0x00):
        self.it_len=len
        self.it_present=bitmap
        self.rate=r
        self.tx_power=t
        self.antenna=a
    def Header(self):
        'Returns the standard Radio Tap header'
        return pack('!BBHLBBB',self.it_version,self.it_pad,htons(self.it_len),htonl(self.it_present),self.rate,self.tx_power,self.antenna)

def BuildRTHeader(list):
    'Expects a list of Radio Tap fields, properly ordered according to standards. Only to be used when the standard header is insufficient, for example when using monitor mode injections over a virtual interface or over using some NICs that have this requirement'
    pass    
