#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


# TODO refatorar essa classe para outro arquivo
class LinuxRouter(Node):
    """
    A Node with IP forwarding enabled.
    Source: https://github.com/mininet/mininet/blob/master/examples/linuxrouter.py#L38
    """

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def __init__(self):
        super(NetworkTopo, self).__init__()
        
        gw = '192.168.0.254/24'  # IP address for r0-eth1

        # router
        router = self.addNode('r0', cls=LinuxRouter, ip=gw)

        # switch
        s1 = self.addSwitch('s1')

        # hosts
        h1 = self.addHost('h1', ip='192.168.0.1/24',
                           defaultRoute=gw)
        h2 = self.addHost('h2', ip='192.168.0.2/24',
                           defaultRoute=gw)

        # links
        self.addLink(s1, router, intfName1='s1-eth1', intfName2='r0-eth1')

        for h, s in [ (h1, s1), (h2, s1) ]:
            self.addLink(h, s)


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()
    
    net.pingAll()
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
