#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, info, setLogLevel
from mininet.util import dumpNodeConnections, quietRun, moveIntf
from mininet.cli import CLI
from mininet.node import Switch, OVSKernelSwitch, Node

from subprocess import Popen, PIPE, check_output
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os
import termcolor as T
import time

import dhcp
import util

def log(s, col="green"):
    print T.colored(s, col)


class Router(Switch):
    """Defines a new router that is inside a network namespace so that the
    individual routing entries don't collide.

    """
    ID = 0
    def __init__(self, name, **kwargs):
        kwargs['inNamespace'] = True
        super(Router, self).__init__(name, **kwargs)
        self.controlIntf = Node.defaultIntf(self)
        Router.ID += 1
        self.switch_id = Router.ID

    @staticmethod
    def setup():
        return

    def start(self, controllers):
        pass

    def stop(self):
        self.deleteIntfs()

    def log(self, s, col="magenta"):
        print T.colored(s, col)


class DHCP_server(Node):
    def __init__(self, name, ip_range, gw, **kwargs):
        super(DHCP_server, self).__init__(name, **kwargs)
        self.ip_range = ip_range
        self.gw = gw


def filter_routers(routers):
    return filter(lambda r : isinstance(r, Router), routers)


class Lab3Topo(Topo):
    def __init__(self):
        super(Lab3Topo, self).__init__()

        # routers
        routers = ['RJ0', 'SP0', 'BH0']
        for router in routers:
            self.addSwitch(router, cls=Router)

        # switches
        switches = ['RJ_10', 'RJ_20',
                    'SP_30', 'SP_40',
                    'MG_50', 'MG_60',
                   ]
        
        for switch in switches:
            self.addSwitch(switch)

        # DHCP servers
        for idx in range(10, 70, 10):
            self.addNode('D_%d' % idx,
                     cls=DHCP_server,
                     ip='172.16.%d.253/24' % idx,
                     gw='172.16.%d.254' % idx,
                     ip_range=['172.16.%d.1' % idx,
                               '172.16.%d.252' % idx])

        # hosts
        for switch in range(1, 7):
            for host in range(1, 3):
                self.addHost('h%ds%d' % (host, switch))

        # links
        links = [ ('SP_30', 'h2s3'), ('SP0', 'SP_30'),  ('SP0', 'SP_40'),
                  ('SP_40', 'h1s4'), ('SP_40', 'h2s4'), ('RJ_10', 'h1s1'),
                  ('RJ_10', 'h2s1'), ('RJ_20', 'h1s2'), ('RJ_20', 'h2s2'),
                  ('RJ0', 'RJ_10'),  ('RJ0', 'RJ_20'),  ('SP_30', 'h1s3'),
                  ('RJ0', 'SP0'),    ('BH0', 'MG_50'),  ('BH0', 'MG_60'),
                  ('MG_60', 'h1s6'), ('MG_60', 'h2s6'), ('MG_50', 'h1s5'),
                  ('MG_50', 'h2s5'), ('SP0', 'BH0'),
                  ('D_10', 'RJ_10'), ('D_20', 'RJ_20'), ('D_30', 'SP_30'),
                  ('D_40', 'SP_40'), ('D_50', 'MG_50'), ('D_60', 'MG_60'), 
                ]

        for link in links:
            self.addLink(*link)
        

def main():
    util.init_clean_up()
    dhcp.check_required()
    
    net = Mininet(topo=Lab3Topo())
    
    info( '*** Starting network\n')
    net.start()

    # init routers
    util.init_routers(filter_routers(net.switches))

    servers = filter(lambda h : isinstance(h, DHCP_server), net.hosts)
    clients = filter(lambda h : not isinstance(h, DHCP_server), net.hosts)

    dhcp.init_dhcp(servers, clients)
    
    CLI(net)
    
    dhcp.exit_clean_up(servers, clients)
    net.stop()
    util.exit_clean_up()

'''
manual ping

RJ0 ping -c 1 h1s1
RJ0 ping -c 1 h2s1
RJ0 ping -c 1 h1s2
RJ0 ping -c 1 h2s2

SP0 ping -c 1 h1s3
SP0 ping -c 1 h2s3
SP0 ping -c 1 h1s4
SP0 ping -c 1 h2s4

BH0 ping -c 1 h1s5
BH0 ping -c 1 h2s5
BH0 ping -c 1 h1s6
BH0 ping -c 1 h2s6
'''


if __name__ == "__main__":
    setLogLevel( 'info' )
    main()

