from mininet.node import Switch

class Router(Switch):
    """
    Defines a new router that is inside a network namespace so that the
    individual routing entries don't collide.

    Source: laboratorio BGP
    """
    ID = 0
    def __init__(self, name, **kwargs):
        kwargs['inNamespace'] = True
        super(Router, self).__init__(name, **kwargs)
        Router.ID += 1
        self.switch_id = Router.ID

    @staticmethod
    def setup():
        return

    def start(self, controllers):
        pass

    def stop(self):
        self.deleteIntfs()
