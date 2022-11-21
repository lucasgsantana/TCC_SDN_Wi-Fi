import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import RemoteController
from mn_wifi.node import OVSKernelAP

N_hosts = 8

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
    info("*** Creating network\n")
    net = Mininet_wifi(controller = RemoteController,accessPoint=OVSKernelAP)

    info("*** Adding stations to the topology\n")
    for i in range (int(N_hosts/2)):
        net.addStation(Hosts_Array[i].name, mac=Hosts_Array[i].mac, ip=Hosts_Array[i].ip,
                   min_x=-10, max_x=30, min_y=10, max_y=50, min_v=1, max_v=3,txpower=11,
                   bgscan_threshold=-60, s_inverval=1, l_interval=3, bgscan_module="simple")

    for i in range (int(N_hosts/2+1), int(N_hosts)):
        net.addStation(Hosts_Array[i].name, mac=Hosts_Array[i].mac, ip=Hosts_Array[i].ip,
                   min_x=0, max_x=70, min_y=10, max_y=50, min_v=1, max_v=1,txpower=11,
                   bgscan_threshold=-60, s_inverval=1, l_interval=3, bgscan_module="simple")

    info("*** Adding 2 APs and controllers\n")

    ap1 = net.addAccessPoint('ap1', ssid='handover', channel='1',mode='n2',passwd='123456789a', position='15,30,0',txpower=18,encrypt='wpa2')
    ap2 = net.addAccessPoint('ap2', ssid='handover', channel='6',mode='n2',passwd='123456789a', position='60,30,0',txpower=18,encrypt='wpa2')
    c1 = net.addController('c1', controller=RemoteController)

    net.setPropagationModel(model="logDistance", exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, ap2)

    net.plotGraph(min_x=-20,max_x=85,min_y=-10,max_y=80)
    net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)