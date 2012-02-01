from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
import sys

class EvalProtocol(LineReceiver):

    def __init__(self):
        sys.stdout.write("Created\n")

    def connectionMade(self):
        sys.stdout.write("Connection made\n")

    def connectionLost(self, reason):
        sys.stdout.write("Connection lost\n")

    def lineReceived(self, line):
        sys.stdout.write(line + " = ")
        result = str(eval(line))
        sys.stdout.write(result + "\n")

class EvalFactory(Factory):
    def buildProtocol(self, addr):
        return EvalProtocol()
