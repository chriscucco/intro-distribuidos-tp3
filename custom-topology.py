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
            takenSwitchs = int(math.pow(2, i-2))
            destinySwitches = 2 * takenSwitchs
            initialMove = takenSwitchs - 1

            ## Left branch
            initialSwitch = int(initialMove)
            lastLeftSwitch = int(initialMove + takenSwitchs)
            lastRightSwitch = int(lastLeftSwitch + destinySwitches)

            leftSwitches = []
            rightSwitches = []

            index = initialSwitch
            while index < lastLeftSwitch:
                leftSwitches.append(switches[int(index)])
                index += 1
            
            while index < lastRightSwitch:
                rightSwitches.append(switches[int(index)])
                index += 1

            leftBranchIndex = 0
            while leftBranchIndex < len(leftSwitches):
                self.addLink(leftSwitches[leftBranchIndex], rightSwitches[(2*leftBranchIndex)])
                self.addLink(leftSwitches[leftBranchIndex], rightSwitches[(2*leftBranchIndex)+1])
                leftBranchIndex += 1

            ## Right branch
            initialSwitch = int(-1-initialMove)
            lastLeftSwitch = int(-1 - initialMove - takenSwitchs)
            lastRightSwitch = int(lastLeftSwitch - destinySwitches)

            leftSwitches = []
            rightSwitches = []
            index = initialSwitch
            while index > lastLeftSwitch:
                leftSwitches.append(switches[int(index)])
                index -= 1
            
            while index > lastRightSwitch:
                rightSwitches.append(switches[int(index)])
                index -= 1
            
            rightBranchIndex = 0
            while rightBranchIndex < len(leftSwitches):
                self.addLink(leftSwitches[rightBranchIndex], rightSwitches[(2*rightBranchIndex)])
                self.addLink(leftSwitches[rightBranchIndex], rightSwitches[(2*rightBranchIndex)+1])
                rightBranchIndex += 1
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
