from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
import sys

class EvalProtocol(LineReceiver):

    def __init__(self, object_store):
        sys.stdout.write("Created\n")
        self.object_store = object_store

    def connectionMade(self):
        sys.stdout.write("Connection made\n")

    def connectionLost(self, reason):
        sys.stdout.write("Connection lost\n")

    def lineReceived(self, line):
        sys.stdout.write(line + " = ")
        result = eval(line)
        sys.stdout.write(str(result) + "\n")

        if not isinstance(result, dict):
            print "Not a dictionary, discarding"
        else:
            self.object_store.append(result)
            print self.object_store

class EvalFactory(Factory):
    def __init__(self):
        self.object_store = []

    def buildProtocol(self, addr):
        return EvalProtocol(self.object_store)
