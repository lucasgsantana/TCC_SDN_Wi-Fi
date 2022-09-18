#!/usr/bin/env python

'Setting the position of Nodes and providing mobility using mobility models'
import sys

from mininet.log import setLogLevel, info
from mininet.node import Controller
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

N_hosts = 30

class Host:
    def __init__(self,name, mac, ip):
        self.name = name
        self.mac = mac
        self.ip = ip

Hosts_Array = []

for i in range (N_hosts):
    Nsta = i+1
    NIP = i+2
    Nmac = i+2
    CurrentHost = Host('sta' + str(Nsta),'00:00:00:00:00:0' + str(Nmac),'10.0.0.' + str(NIP) + '/8')
    Hosts_Array.append(CurrentHost)


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller = Controller,accessPoint=OVSKernelAP)

    info("*** Creating N nodes\n")

    for i in range (N_hosts):
        net.addStation(Hosts_Array[i].name, mac=Hosts_Array[i].mac, ip=Hosts_Array[i].ip,
                   min_x=20, max_x=80, min_y=20, max_y=80, min_v=1, max_v=3,txpower=50)


    ap1 = net.addAccessPoint('ap1',ssid='ssid-ap1',channel='36',mode='ax5',position='50,50,0',txpower=50)
    c1 = net.addController('c1')
    net.setPropagationModel(model="logDistance",exp=6)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()
    net.plotGraph(max_x=100,max_y=100)

    net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)