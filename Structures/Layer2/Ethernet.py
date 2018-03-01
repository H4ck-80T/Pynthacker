'''
Creates an Ethernet Frame to be injected over the network. The arguments are expected in the same order in which they appear in the Ethernet Frame. Destination, Source, Ether Type.
'''

from struct import pack
from socket import htons


def make(base):
    base=base.split(':')
    d=''
    for item in base:
        d+=chr(int(item,16))
    return d


class EthernetFrame():
    def __init__(self,smac,dmac,proto):
        self.destination_mac=make(dmac)
        self.source_mac=make(smac)
        self.ether_type=proto
    def Frame(self):
        return pack('!6s6sH',self.destination_mac,self.source_mac,self.ether_type)
