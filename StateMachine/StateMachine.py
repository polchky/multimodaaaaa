# StateMachine/StateMachine.py
# Takes a list of Inputs to move from State to
# State using a template method.

class StateMachine:
    def __init__(self, initialState):
        self.currentState = initialState
        self.currentState.onStart()
        self.currentState.run()
    # Template method:
    def run(self):
        while True:
            nextState = self.currentState.next()
            if nextState != self.currentState:
                self.currentState.onStop()
                self.currentState = nextState
                self.currentState.onStart()
            self.currentState.run()