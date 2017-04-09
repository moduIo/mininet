"""
Example topology of Quagga routers
"""

import inspect
import os
from mininext.topo import Topo
from mininext.services.quagga import QuaggaService

from collections import namedtuple

QuaggaHost = namedtuple("QuaggaHost", "name ip loIP type")
net = None


class QuaggaTopo(Topo):

    "Creates a topology of Quagga routers"

    def __init__(self):
        """Initialize a Quagga topology with 4 routers and 2 hosts, 
           configure their IP addresses, loop back interfaces, 
           and paths to their private configuration directories."""
        Topo.__init__(self)

        # Directory where this file / script is located"
        selfPath = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))  # script directory

        # Initialize a service helper for Quagga with default options
        quaggaSvc = QuaggaService(autoStop=False)

        # Path configurations for mounts
        quaggaBaseConfigPath = selfPath + '/configs/'

        # List of Quagga host configs
        quaggaHosts = []
        quaggaHosts.append(QuaggaHost(name='r1', ip='172.0.1.2/24',
                                      loIP='10.0.1.1/24', type='switch'))
        quaggaHosts.append(QuaggaHost(name='r2', ip='172.0.2.2/24',
                                      loIP='10.0.2.1/24', type='switch'))
        quaggaHosts.append(QuaggaHost(name='r3', ip='172.0.3.2/24',
                                      loIP='10.0.3.1/24', type='switch'))
        quaggaHosts.append(QuaggaHost(name='r4', ip='172.0.4.2/24',
                                      loIP='10.0.4.1/24', type='switch'))
        
        quaggaHosts.append(QuaggaHost(name='h1', ip='172.0.1.1/24',
                                      loIP='10.0.1.1/24', type='host'))
        quaggaHosts.append(QuaggaHost(name='h2', ip='172.0.6.2/24',
                                      loIP='10.0.6.1/24', type='host'))

        # Add switch for IXP fabric
        #ixpfabric = self.addSwitch('fabric-sw1')

	containers = []

        # Setup each Quagga router
        for host in quaggaHosts:

            # Create an instance of a host, called a quaggaContainer
	    if host.type != 'xhost':
                quaggaContainer = self.addHost(name=host.name,
                                               ip=host.ip,
                                               hostname=host.name,
                                               privateLogDir=True,
                                               privateRunDir=True,
                                               inMountNamespace=True,
                                               inPIDNamespace=True,
                                               inUTSNamespace=True)
	    else:
		quaggaContainer = self.addSwitch(name=host.name,
					         ip=host.ip,
                                                 hostname=host.name,
					         privateLogDir=True,
                                                 privateRunDir=True,
					         inMountNamespace=True,
					         inPIDNamespace=True,
					         inUTSNamespace=True)

	    containers.append(quaggaContainer)

            # Add a loopback interface with an IP in router's announced range
            self.addNodeLoopbackIntf(node=host.name, ip=host.loIP)

            # Configure and setup the Quagga service for this node
            quaggaSvcConfig = \
                {'quaggaConfigPath': quaggaBaseConfigPath + host.name}
            self.addNodeService(node=host.name, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)

            # Attach the quaggaContainer to the IXP Fabric Switch
            #self.addLink(quaggaContainer, ixpfabric)
	
	# Manually assign links
	self.addLink(containers[0], containers[4])
	self.addLink(containers[0], containers[1])
	self.addLink(containers[0], containers[2])
	self.addLink(containers[1], containers[3])
	self.addLink(containers[2], containers[3])
	self.addLink(containers[3], containers[5])
