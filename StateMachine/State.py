# StateMachine/State.py
# A State has an operation, and can be moved
# into the next State given an Input:

class State:
    def run(self):
        assert 0, "run not implemented"
    def next(self):
        assert 0, "next not implemented"
    def onStart(self):
        assert 0, "onStart not implemented"
    def onExit(self):
        assert 0, "onExit not implemented"