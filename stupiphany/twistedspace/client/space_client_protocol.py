from twisted.internet import defer
from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver

class SpaceClientProtocol(LineReceiver):
    def put(self, dict):
        self.sendLine("PUT:" + str(dict))
        self._waiting = defer.Deferred()

        return self._waiting

    def lineReceived(self, line):
        if self._waiting is not None:
            self._waiting.callback(None)

class SpaceClientFactory(Factory):
    def buildProtocol(self, addr):
        return SpaceClientProtocol()