import os
from time import sleep, time
from mininet.log import lg, info, setLogLevel

import termcolor as T

def log(s, col="green"):
    print T.colored(s, col)


def init_clean_up():
    os.system("rm -f /tmp/R*.log /tmp/R*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")
    os.system("killall -9 zebra bgpd > /dev/null 2>&1")
    os.system('pgrep -f webserver.py | xargs kill -9')


def exit_clean_up():
    os.system("killall -9 zebra bgpd")
    os.system('pgrep -f webserver.py | xargs kill -9')


def init_routers(routers, sleep_time=3):
    for router in routers:
        log('initing router %s' % router)
        router.cmd("sysctl -w net.ipv4.ip_forward=1")
        router.waitOutput()

    log("Waiting %d seconds for sysctl changes to take effect..."
        % sleep_time)
    sleep(sleep_time)

    for router in routers:    
        router.cmd("/usr/lib/quagga/zebra -f conf/zebra-%s.conf -d -i /tmp/zebra-%s.pid > logs/%s-zebra-stdout 2>&1" % (router.name, router.name, router.name))
        router.waitOutput()
        router.cmd("/usr/lib/quagga/bgpd -f conf/bgpd-%s.conf -d -i /tmp/bgp-%s.pid > logs/%s-bgpd-stdout 2>&1" % (router.name, router.name, router.name), shell=True)
        router.waitOutput()
