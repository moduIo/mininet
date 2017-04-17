#!/usr/bin/python

"""
Example network of Quagga routers
(QuaggaTopo + QuaggaService)
"""

import sys
import atexit

# patch isShellBuiltin
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

from mininet.util import dumpNodeConnections
from mininet.node import OVSController
from mininet.log import setLogLevel, info

from mininext.cli import CLI
from mininext.net import MiniNExT

from topo import QuaggaTopo

net = None

def startNetwork():
    "instantiates a topo, then starts the network and prints debug information"

    info('** Creating Quagga network topology\n')
    topo = QuaggaTopo()

    info('** Starting the network\n')
    global net
    net = MiniNExT(topo, controller=OVSController)
    net.start()

    # Manually add interface IP addresses
    print '** Adding interface IP addresses\n'
    r1 = net.getNodeByName('r1')
    r1.setIP('172.0.2.1/24', 24, 'r1-eth1')
    r1.setIP('172.0.3.1/24', 24, 'r1-eth2')

    r2 = net.getNodeByName('r2')
    r2.setIP('172.0.4.1/24', 24, 'r2-eth1')

    r3 = net.getNodeByName('r3')
    r3.setIP('172.0.5.1/24', 24, 'r3-eth1')

    r4 = net.getNodeByName('r4')
    r4.setIP('172.0.5.2/24', 24, 'r4-eth1')
    r4.setIP('172.0.6.1/24', 24, 'r4-eth2')

    h1 = net.getNodeByName('h1')
    h2 = net.getNodeByName('h2')
    
    # Enable forwarding on each host
    r1.cmd('sysctl net.ipv4.ip_forward=1')
    r2.cmd('sysctl net.ipv4.ip_forward=1')
    r3.cmd('sysctl net.ipv4.ip_forward=1')
    r4.cmd('sysctl net.ipv4.ip_forward=1')
    h1.cmd('sysctl net.ipv4.ip_forward=1')
    h2.cmd('sysctl net.ipv4.ip_forward=1')

    # Start servers
    info('** Starting servers on port 800\n')
    r1.cmd('python rip_lite_server.py "h1,r2,r3" "172.0.1.1,172.0.2.2,172.0.3.2" &')
    r2.cmd('python rip_lite_server.py "r1,r4" "172.0.2.1,172.0.4.2" &')
    r3.cmd('python rip_lite_server.py "r1,r4" "172.0.3.1,172.0.5.2" &')
    r4.cmd('python rip_lite_server.py "r2,r3,h2" "172.0.4.1,172.0.5.1,172.0.6.2" &')
    h1.cmd('python rip_lite_server.py "r1" "172.0.1.2" &')
    h2.cmd('python rip_lite_server.py "r4" "172.0.6.1" &')

    # Start CLI
    info('** Running CLI\n')
    CLI(net)

def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
