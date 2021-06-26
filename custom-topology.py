from mininet.topo import Topo
import math
import sys

class CustomTopo(Topo):
    def build(self, levels, hosts):
        numOfSwitches = self.calculateNumOfSwitches(int(levels))
        print('//////////////////////')
        print(numOfSwitches)
        print('//////////////////////')
        return

    def calculateNumOfSwitches(self, levels):
        sum = math.pow(2, levels - 1)
        while ( 0 < levels -1):
            sum += math.pow(2, levels - 1)
            levels -= 1
        return sum

topos = { 'custom': (lambda x,y: CustomTopo(x,y))}
