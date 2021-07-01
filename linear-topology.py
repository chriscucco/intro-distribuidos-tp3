from mininet.topo import Topo
import math

class LinearCustomTopo(Topo):
    def build(self, switchesNum):
        print('//////////////////////')
        numOfSwitches = int(switchesNum)
        switches = []
        print('Creating host h1')
        h1 = self.addHost('h1')
        print('Creating host h2')
        h2 = self.addHost('h2')
        print('Creating host h3')
        h3 = self.addHost('h3')
        print('Creating host h4')
        h4 = self.addHost('h4')

        i = 1
        while numOfSwitches > 0:
            switchName = 's'+str(i)
            print('Creating switch '+switchName)
            s = self.addSwitch(switchName)
            switches.append(s)
            numOfSwitches -= 1
            i += 1
        
        print('Connecting hosts to switches')
        firstSwitch = switches[0]
        lastSwitch = switches[-1]
        self.addLink(h1, firstSwitch)
        self.addLink(h2, firstSwitch)
        self.addLink(h3, lastSwitch)
        self.addLink(h4, lastSwitch)

        print('Connecting between switches')
        i = 1
        while i < len(switches):
            self.addLink(switches[i-1], switches[i])
            i += 1
        print('//////////////////////')
        return

topos = { 'linearCustom': (lambda x: LinearCustomTopo(x))}
