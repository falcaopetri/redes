# Source: lab de dhcp rougue

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.util import quietRun
from mininet.log import setLogLevel, info, lg
from mininet.term import makeTerms
from mininet.examples.nat import connectToInternet, stopNAT

from sys import exit, stdin, argv
from re import findall
from time import sleep
import os

import termcolor as T

def log(s, col="green"):
    print T.colored(s, col)
    
def check_required():
    "Check for required executables"
    required = [ 'udhcpd', 'udhcpc', 'dnsmasq', 'curl', 'firefox' ]
    for r in required:
        if not quietRun( 'which ' + r ):
            print '* Installing', r
            print quietRun( 'apt-get install -y ' + r )
            if r == 'dnsmasq':
                # Don't run dnsmasq by default!
                print quietRun( 'update-rc.d dnsmasq disable' )

# DHCP server functions and data

def makeDHCPconfig( filename, intf, gw, dns, start, end):
    "Create a DHCP configuration file"
    config = (
        'interface %s' % intf,
        'start %s' % start,
        'end %s' % end,
        'option  subnet  255.255.255.0',
        'option  domain  local',
        'option  lease   7  # seconds',
        'option router %s' % gw,
        'option dns %s' % dns,
        '' )
    with open( filename, 'w' ) as f:
        f.write( '\n'.join( config ) )


def startDHCPserver( host, gw, dns ):
    "Start DHCP server on host with specified DNS server"
    info( '* Starting DHCP server on', host, 'at', host.IP(), '\n' )
    dhcpConfig = '/tmp/%s-udhcpd.conf' % host
    makeDHCPconfig(dhcpConfig, host.defaultIntf(), gw, dns, *host.ip_range)
    host.cmd( 'udhcpd -f', dhcpConfig,
              '1>/tmp/%s-dhcp.log 2>&1  &' % host )


def stopDHCPserver( host ):
    "Stop DHCP server on host"
    info( '* Stopping DHCP server on', host, 'at', host.IP(), '\n' )
    host.cmd( 'kill %udhcpd' )


def startDHCPclient( host ):
    "Start DHCP client on host"
    intf = host.defaultIntf()
    host.cmd( 'dhclient -v -d -r', intf )
    host.cmd( 'dhclient -v -d 1> /tmp/%s-dhclient.log 2>&1' % host.name, intf, '&' )


def stopDHCPclient( host ):
    host.cmd( 'kill %dhclient' )


def waitForIP( host ):
    "Wait for an IP address"
    info( '*', host, 'waiting for IP address' )
    while True:
        host.defaultIntf().updateIP()
        if host.IP():
            break
        info( '.' )
        sleep( 1 )
    info( '\n' )
    info( '*', host, 'is now using',
          host.cmd( 'grep nameserver /etc/resolv.conf' ) )


def mountPrivateResolvconf(host):
    "Create/mount private /etc/resolv.conf for host"
    etc = '/tmp/etc-%s' % host
    host.cmd( 'mkdir -p', etc )
    host.cmd( 'mount --bind /etc', etc )
    host.cmd( 'mount -n -t tmpfs tmpfs /etc' )
    host.cmd( 'ln -s %s/* /etc/' % etc )
    host.cmd( 'rm /etc/resolv.conf' )
    host.cmd( 'cp %s/resolv.conf /etc/' % etc )


def unmountPrivateResolvconf(host):
    "Unmount private /etc dir for host"
    etc = '/tmp/etc-%s' % host
    host.cmd( 'umount /etc' )
    host.cmd( 'umount', etc )
    host.cmd( 'rmdir', etc )


def exit_clean_up(servers, clients):
    for server in servers:
        stopDHCPserver(server)

    for client in clients:
        stopDHCPclient(client)
        unmountPrivateResolvconf(client)


def init_dhcp(servers, clients, sleep_time=7):
    for server in servers:
        startDHCPserver(server, gw=server.gw, dns='8.8.8.8')

    log("Waiting %d seconds for startDHCPserver changes to take effect..."
        % sleep_time)
    sleep(sleep_time)
    
    for client in clients:
        mountPrivateResolvconf(client)
        startDHCPclient(client)
        waitForIP(client)
