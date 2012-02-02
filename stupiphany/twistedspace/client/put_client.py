from twisted.internet import reactor
from twisted.python.log import startLogging
from twisted.internet.endpoints import TCP4ClientEndpoint
import sys
from stupiphany.twistedspace.client.space_client_protocol import SpaceClientFactory

def gotProtocol(p):
    d = p.put("dict(name='Bill', age=45)")
    d.addCallback(exitReactor, p)

def exitReactor(ignored, p):
    print "In exitReactor"
    p.transport.loseConnection()
    reactor.stop()

point = TCP4ClientEndpoint(reactor, "localhost", 5425)
d = point.connect(SpaceClientFactory())
d.addCallback(gotProtocol)
startLogging(sys.stdout)
reactor.run()
