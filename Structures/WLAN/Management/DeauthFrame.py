from socket import htons
from struct import pack
from ManagementFrame import ManagementFrame

class DeauthFrame(ManagementFrame):
    'Builds an IEEE 802.11 De-Authentication Frame. The MAC addressess must be passed in the standard order'
    subtype=0x00c0
    flags=0x0000
    duration=htons(0xa301)
    seq_ctrl=htons(0xf000)
    def __init__(self,smac='\xff\xff\xff\xff\xff\xff',dmac='\xff\xff\xff\xff\xff\xff',bss='\xff\xff\xff\xff\xff\xff',code=htons(0x0007)):
        self.destination_mac=dmac
        self.source_mac=smac
        self.bssid=bss
        self.frame_control=htons(self.version|self.type|self.subtype|self.flags)
        self.reason_code=code
    def Deauth(self):
        return pack('!HH6s6s6sHH',self.frame_control,self.duration,self.destination_mac,self.source_mac,self.bssid,self.seq_ctrl,self.reason_code)
