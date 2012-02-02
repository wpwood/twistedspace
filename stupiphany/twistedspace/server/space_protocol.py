from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from stupiphany.twistedspace.server.object_store import ObjectStore
import sys

class SpaceProtocol(LineReceiver):

    def __init__(self, object_store):
        sys.stdout.write("Created\n")
        self.object_store = object_store

    def connectionMade(self):
        sys.stdout.write("Connection made\n")

    def connectionLost(self, reason):
        sys.stdout.write("Connection lost\n")

    def handle_PUT(self, line):
        result = eval(line)
        if not isinstance(result, dict):
            print "Not a dictionary, discarding"
        else:
            self.object_store.put(result)
            print self.object_store

    def handle_GET(self, line):
        request = eval(line)
        if not isinstance(request, dict):
            print "Not a dictionary, discarding"
        else:
            value = self.object_store.get(request)
            print self.object_store
            return value

    def lineReceived(self, line):
        command = line[0:4]
        tuple = line[4:]

        if command == 'PUT:':
            self.handle_PUT(tuple)
            self.sendLine("DONE")
        elif command == 'GET:':
            value = self.handle_GET(tuple)
            self.sendLine(str(value))
        else:
            print("Unrecognized request -- " + line)
            self.sendLine("ERROR")


class SpaceFactory(Factory):
    def __init__(self):
        self.object_store = ObjectStore()

    def buildProtocol(self, addr):
        return SpaceProtocol(self.object_store)
