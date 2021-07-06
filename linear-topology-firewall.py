from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import EventMixin
from pox.lib.addresses import EthAddr
import csv

log = core.getLogger()

LINK_PROTOCOL = 1
SRCMAC = 2
DSTMAC = 3
NETWORK_PROTOCOL = 4
SRCIP = 5
DSTIP = 6
TRANSPORT_PROTOCOL = 7
SRCPORT = 8
DSTPORT = 9


class Firewall (EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        self.droppingRules = []
        self.switchesWithRules = {}
        self._parseDroppingRules()
        self._parseSwitchesWithRules()
        log.debug("Enabling Firewall Module ")

    def _parseDroppingRules(self):
        with open('dropping_rules.csv', 'r') as f:
            reader = csv.reader(f)
            i = 0

            for row in reader:
                if i == 0:
                    i += 1
                    continue

                self.droppingRules.append([row[LINK_PROTOCOL], row[SRCMAC],
                                          row[DSTMAC], row[NETWORK_PROTOCOL],
                                          row[SRCIP], row[DSTIP],
                                          row[TRANSPORT_PROTOCOL],
                                          row[SRCPORT], row[DSTPORT]])
                i += 1

    def _parseSwitchesWithRules(self):
        with open('switches_with_rules.csv', 'r') as f:
            reader = csv.reader(f)
            i = 0

            for row in reader:
                if i == 0:
                    i += 1
                    continue

                self.switchesWithRules[int(row[0])] = row[0]
                i += 1

    def _checkRules(self, event):

        drop = False

        for rule in self.droppingRules:

            packet = event.parsed

            link_layer = packet.find(rule[LINK_PROTOCOL-1])

            if not link_layer:
                continue

            if rule[SRCMAC-1] and str(link_layer.src) != str(rule[SRCMAC-1]):
                continue

            if rule[DSTMAC-1] and str(link_layer.dst) != str(rule[DSTMAC-1]):
                continue

            network_layer = packet.find(rule[NETWORK_PROTOCOL-1])

            if not network_layer:
                continue

            if (rule[SRCIP-1] and str(network_layer.srcip) !=
                    str(rule[SRCIP-1])):
                continue

            if (rule[DSTIP-1] and str(network_layer.dstip)
                    != str(rule[DSTIP-1])):
                continue

            transport_layer = packet.find(rule[TRANSPORT_PROTOCOL-1])

            if not transport_layer:
                continue

            if (rule[SRCPORT-1] and str(transport_layer.srcport) !=
                    str(rule[SRCPORT-1])):
                continue

            if (rule[DSTPORT-1] and str(transport_layer.dstport) !=
                    str(rule[DSTPORT-1])):
                continue

            drop = True
            log.debug("Packet dropped with data:")
            log.debug("**" + str(link_layer))
            log.debug("**" + str(network_layer))
            log.debug("**" + str(transport_layer))
            break

        return drop

    def _handle_PacketIn(self, event):
        if event.dpid in self.switchesWithRules:
            drop = self._checkRules(event)
            if drop is True:
                event.halt = True

        return

    def _blockHosts(self, event):
        with open('blocking_rules.csv', 'r') as f:
            reader = csv.reader(f)
            i = 0

            for row in reader:
                if i == 0:
                    i += 1
                    continue
                blocked = of.ofp_match()
                blocked.dl_src = EthAddr(row[1])
                blocked.dl_dst = EthAddr(row[2])
                flow_mod = of.ofp_flow_mod()
                flow_mod.match = blocked
                event.connection.send(flow_mod)
                log.debug(str(row[1]) + " and " + str(row[2]) + " blocked.")
                i += 1

    def _handle_ConnectionUp(self, event):
        if event.dpid in self.switchesWithRules:
            self._blockHosts(event)
        return


def launch():
    # Starting the Firewall module
    core.registerNew(Firewall)
