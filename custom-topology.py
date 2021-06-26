from mininet.topo import Topo
import sys

class CustomTopo(Topo):
    def build(self, levels, hosts):
        print('AAAAAAAAAAAAAAAA')
        print(levels)
        print(hosts)
        print(sys.argv)
        return

topos = { 'custom': (lambda x,y: CustomTopo(x,y))}
