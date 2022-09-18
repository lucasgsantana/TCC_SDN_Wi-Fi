import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology(args):
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01',ip='10.0.0.2/8',
    min_x=10, max_x=50, min_y=15, max_y=50, min_v=1, max_v=1)
    
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02',ip='10.0.0.3/8',
    min_x=10, max_x=25, min_y=20, max_y=40, min_v=1, max_v=1)

    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', channel='1', position='15,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', channel='6', position='55,30,0')
    c1 = net.addController('c1')

    net.setPropagationModel(model="logDistance", exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, ap2)

    net.plotGraph(min_x=-20,max_x=85,min_y=-10,max_y=80)
    net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20,ac_method='llf')

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