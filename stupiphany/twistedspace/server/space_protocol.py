from twisted.internet import defer
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from stupiphany.twistedspace.server.object_store import ObjectStore
import sys

class SpaceProtocol(LineReceiver):

    def __init__(self, object_store, pending_gets):
        self._object_store = object_store
        self._pending_gets = pending_gets

    def connectionMade(self):
        sys.stdout.write("Connection made\n")

    def connectionLost(self, reason):
        sys.stdout.write("Connection lost\n")

    def handle_PUT(self, line):
        result = eval(line)
        if not isinstance(result, dict):
            print "Not a dictionary, discarding"
            self.sendLine("ERROR")
        else:
            self._object_store.put(result)
            print self._object_store
            print self._pending_gets
            for pg in self._pending_gets:
                print pg
                value = self._object_store.get(pg['request'])
                if value != None:
                    d = pg['deferred']
                    self._pending_gets.remove(pg)
                    d.callback(value)
            self.sendLine("DONE")

    def handle_GET(self, line):
        request = eval(line)
        if not isinstance(request, dict):
            print "Not a dictionary, discarding"
            self.sendLine("ERROR")
        else:
            value = self._object_store.get(request)
            if value == None:
                print "Pending match, " + str(request)

                d = defer.Deferred()
                d.addCallback(self.pendingSend)
                self._pending_gets.append(dict(request=request, deferred=d))
                print self._pending_gets
            else:
                print self._object_store
                self.sendLine(str(value))

    def pendingSend(self, result):
        self.sendLine(str(result))

    def lineReceived(self, line):
        command = line[0:4]
        tuple = line[4:]

        if command == 'PUT:':
            self.handle_PUT(tuple)
        elif command == 'GET:':
            self.handle_GET(tuple)
        else:
            print("Unrecognized request -- " + line)
            self.sendLine("ERROR")


class SpaceFactory(Factory):
    def __init__(self):
        self._object_store = ObjectStore()
        self._pending_gets = []

    def buildProtocol(self, addr):
        return SpaceProtocol(self._object_store, self._pending_gets)
