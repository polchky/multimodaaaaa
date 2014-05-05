import uinput, time
from glove import Glove


class Joystick:
    ANALOG = 0
    BUTTON = 1
    MIN_PRESS_TIME = 200 # milliseconds
    MIN_REPRESS_TIME = 700 # milliseconds
    DEFAULT_ACTIONS = {
        'X': (uinput.ABS_X, ANALOG),
        'Y': (uinput.ABS_Y, ANALOG),
        'RX': (uinput.ABS_RX, ANALOG),
        'RY': (uinput.ABS_RY, ANALOG),
        'para': (uinput.BTN_0, BUTTON),
        'graf': (uinput.BTN_1, BUTTON),
        'fuck': (uinput.BTN_2, BUTTON),
        'yeah': (uinput.BTN_3, BUTTON),
        'walk': (uinput.KEY_W, BUTTON)
    }
    
    def __init__(self, actions=DEFAULT_ACTIONS, name='Gamepad'):
        self.actions = actions
        self.state = dict.fromkeys(actions, 0)
        self.device = uinput.Device([a[0] for a in actions.values()], name)
        self.parachute_opened = False
        self.last_gesture = Glove.OPEN
        self.last_time_pressed = 0
        self.last_time_changed = 0
        self.ready_to_graffiti = False
    """
    def update(self, XY, fingers):
        for k in actions:
            self.emit(k, actions[k])
        self.device.syn()
    """
    def update_buttons(self, fingers):
        if fingers not in self.actions.values():
            self.last_gesture = fingers
            return
        if fingers == self.last_gesture:
            if self.check_last_changed() and self.check_last_pressed():
                self.emit_from_fingers(fingers)
                self.last_time_pressed = self.get_time()
        else:
            self.last_time_changed = self.get_time()
            self.last_gesture = fingers
            if fingers != Glove.FINGER_POSITIONS['FIST']:
                self.ready_to_graffiti = False
             
    def emit_from_fingers(self, fingers):
        if fingers == Glove.FINGER_POSITIONS['FUCK']:self.emit(self.actions['fuck'], 1)
        elif fingers == Glove.FINGER_POSITIONS['YEAH']:self.emit(self.actions['yeah'], 1)
        elif fingers == Glove.FINGER_POSITIONS['GRAF']:self.ready_to_graffiti = True
        elif fingers == Glove.FINGER_POSITIONS['FIST'] and self.ready_to_graffiti:
            self.emit(self.actions['graf'], 1)
            self.ready_to_graffiti = False
            
         
    def update_joystick(self, XY):
        
    def walk(self,fingers):
        if self.last_gesture == Glove.FINGER_POSITIONS['OPEN']:
            self.device.emit(self.actions['walk'][0], 1, False)
        if fingers == Glove.FINGER_POSITIONS['OPEN']:
            self.device.emit(self.actions['walk'][0], 0)
            self.last_time_changed = self.get_time()
        self.last_gesture = fingers
        
    def is_walking(self):
        return self.last_gesture != Glove.FINGER_POSITIONS['OPEN']
        
    def reset(self):
        for action in self.actions:
            self.emit(action, 0)

    def emit(self, k, v, syn=False):
        if k not in self.actions:
            return
        if self.actions[k][1] == Joystick.ANALOG:
            self.device.emit(self.actions[k][0], v, syn)
        elif self.actions[k][1] == Joystick.BUTTON and v != 0:
            self.device.emit_click(self.actions[k][0], syn)
            
    def is_parachute_opened(self):
        return self.parachute_opened
        
    def get_time(self):
        return int(round(time.time() * 1000))
        
    def check_last_pressed(self):
        return self.get_time() - self.last_time_pressed > self.MIN_REPRESS_TIME
        
    def check_last_changed(self):
        return self.get_time() - self.last_time_changed > self.MIN_PRESS_TIME