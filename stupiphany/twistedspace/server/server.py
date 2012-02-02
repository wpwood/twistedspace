from twisted.internet import reactor
from stupiphany.twistedspace.server.space_protocol import SpaceFactory

def up_and_running():
    print "Up and running"

reactor.listenTCP(5425, SpaceFactory())

reactor.callWhenRunning(up_and_running)
reactor.run()