from mininet.topo import Topo
import math

class CustomTopo(Topo):
    def build(self, levels, hostsNum):
        numOfSwitches = self.calculateNumOfSwitches(int(levels))
        numOfLevels = int(levels)
        numOfHosts = int(hostsNum)
        switches = []
        hosts = []

        print('//////////////////////')
        i = 1
        while numOfSwitches > 0:
            switchName = 's'+str(i)
            print('Creating switch '+switchName)
            s = self.addSwitch(switchName, failMode='standalone', stp=True)
            switches.append(s)
            numOfSwitches -= 1
            i += 1
        
        i = 1
        while numOfHosts > 0:
            hostName = 'h'+str(i)
            print('Creating host '+hostName)
            h = self.addHost(hostName)
            hosts.append(h)
            numOfHosts -= 1
            i += 1

        print('Hosts and switches created')
        print('Hosts size: '+str(len(hosts)))
        print('Switches size: '+str(len(switches)))
        print('//////////////////////')
        return

    def calculateNumOfSwitches(self, levels):
        sum = math.pow(2, levels - 1)
        while ( 0 < levels -1):
            sum += math.pow(2, levels - 1)
            levels -= 1
        return int(sum)

topos = { 'custom': (lambda x,y: CustomTopo(x,y))}
