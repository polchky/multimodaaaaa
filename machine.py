import time

class Machine:
    def __init__(self, initial):
        self.current = initial
        self.current.on_start()
        self.current.run()
        self.allocated_time = 20 #milliseconds
    # Template method:
    def run(self):
        while True:
            millis = int(round(time.time() * 1000))
            next = self.current.next()
            if next is not self.current:
                self.current.on_stop()
                self.current = next
                self.current.on_start()
            self.current.run()
            time_left = self.allocated_time - (int(round(time.time() * 1000)) - millis)
            if time_left > 0:
                time.sleep(float(time_left)/1000)
            
            
class State:        
    def run(self):
        pass
    
    def next(self):
        return self
        
    def on_start(self):
        pass
    
    def on_exit(self):
        pass