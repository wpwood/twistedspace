from twisted.internet import reactor
from eval_protocol import EvalFactory

def up_and_running():
    print "Up and running"

reactor.listenTCP(5425, EvalFactory())

reactor.callWhenRunning(up_and_running)
reactor.run()