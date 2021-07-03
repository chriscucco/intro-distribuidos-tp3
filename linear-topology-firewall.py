from pox . core import core
import pox . openflow . libopenflow_01 as of
from pox . lib . revent import *
from pox . lib . util import dpidToStr
from pox . lib . addresses import EthAddr
from collections import namedtuple
import os
# Add your imports here ...
log = core . getLogger()

HOST_1 = '00:00:00:00:00:01'
HOST_2 = '00:00:00:00:00:02'
HOST_3 = '00:00:00:00:00:03'


class Firewall (EventMixin):
    def __init__(self):
        self . listenTo(core.openflow)
        log. debug(" Enabling Firewall Module ")

    def _handle_ConnectionUp(self, event):
        # Regla 1: no se pueden comunicar host 2 y 3
        blocked = of.ofp_match()
        blocked.dl_src = EthAddr(HOST_2)
        blocked.dl_dst = EthAddr(HOST_3)
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = blocked
        event.connection.send(flow_mod)

        # Regla 2: descartar paquetes con UDP, puerto 5001 y con src en host1
        '''blocked = of.ofp_match()
        blocked.dl_src = EthAddr(HOST_1)
        blocked.tp_dst = 5001
        blocked.new_proto = 17
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = blocked
        event.connection.send(flow_mod)'''

        # Regla 3: descartar paquetes con puerto 80
        return

    def _handle_PacketIn(self, event):
        blocked = of.ofp_match()
        blocked.tp_dst = 80
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = blocked
        event.connection.send(flow_mod)
        '''
        packet = event.parsed
        if packet.type == packet.IP_TYPE:
            ip_packet = packet.payload
            if ip_packet.protocol == ip_packet.17:

        packet.dst = 80
        '''

        return


def launch():
    # Starting the Firewall module
    core.registerNew(Firewall)
    # core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
