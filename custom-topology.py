from mininet.topo import Topo
import sys

class CustomTopo(Topo):
    def build(self):
        print('AAAAAAAAAAAAAAAA')
        print(sys.argv)
        return

topos = { 'custom': (lambda x,y: CustomTopo())}
