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
        
        print('Connecting hosts to switches')
        for index, host in enumerate(hosts):
            pos = 0
            if (index % 2 > 0):
                pos = -1
            currentSwitch = switches[pos]
            self.addLink(host, currentSwitch)
        
        print('Connecting Switches')
        ## If level = 1, only there is 1 switch and there is no need to
        ## create connections between switches
        i = 2
        while i <= numOfLevels:
            takenSwitchs = math.pow(2, i-2)
            initialMove = takenSwitchs - 0
            print(takenSwitchs)
            print(initialMove)
            i += 1
        print('//////////////////////')
        return

    def calculateNumOfSwitches(self, levels):
        sum = math.pow(2, levels - 1)
        while ( 0 < levels -1):
            sum += math.pow(2, levels - 1)
            levels -= 1
        return int(sum)

topos = { 'custom': (lambda x,y: CustomTopo(x,y))}
