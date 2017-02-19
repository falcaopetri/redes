from mininet.node import Node

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
