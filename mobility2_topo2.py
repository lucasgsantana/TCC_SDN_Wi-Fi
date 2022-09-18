import sys

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import UserAP
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

def topology(args):
    "Create a network."
    net = Mininet_wifi(controller = Controller, accessPoint=UserAP, link=wmediumd,
    wmediumd_mode=interference)

    info("*** Creating nodes\n")

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01',ip='10.0.0.2/8',
    min_x=10, max_x=70, min_y=15, max_y=50, min_v=1, max_v=1,
    bgscan_threshold=-70, s_inverval=2, l_interval=3, bgscan_module="simple")
    
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02',ip='10.0.0.3/8',
    min_x=10, max_x=25, min_y=20, max_y=40, min_v=1, max_v=1,
    bgscan_threshold=-60,s_inverval=2, l_interval=3, bgscan_module="simple",)

    ap1 = net.addAccessPoint('ap1', ssid='handover', channel='1',
    position='15,30,0',passwd='123456789a',mode='g',encrypt='wpa2')
    ap2 = net.addAccessPoint('ap2', ssid='handover', channel='6', 
    position='55,30,0',passwd='123456789a',mode='g',encrypt='wpa2')
    c1 = net.addController('c1')

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