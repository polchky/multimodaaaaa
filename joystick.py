import time

import uinput

from glove import Glove
from constants import RX_FACTOR, X_THRESH, Y_THRESH


class Joystick:
    ANALOG = 0
    BUTTON = 1
    FALSE_ANALOG = 2
    MOUSE = 3

    MIN_PRESS_TIME = 200  # milliseconds
    MIN_REPRESS_TIME = 700  # milliseconds
    ANALOG_RANGE = (-100, 100, 0, 0)

    DEFAULT_ACTIONS_JOYSTICK = {
        'X': (uinput.ABS_X, ANALOG),
        'Y': (uinput.ABS_Y, ANALOG),
        'RX': (uinput.ABS_RY, ANALOG),
        'RY': (uinput.ABS_RX, ANALOG),
        'para': (uinput.KEY_SPACE, BUTTON),
        'graf': (uinput.KEY_LEFTCTRL, BUTTON),
        'fuck': (uinput.BTN_0, BUTTON),
        'yeah': (uinput.BTN_2, BUTTON),
        'walk': (uinput.KEY_W, BUTTON),
        '_': (uinput.BTN_JOYSTICK, BUTTON)
    }

    DEFAULT_ACTIONS_KEYBOARD = {
        'X': ((uinput.KEY_A, uinput.KEY_D), FALSE_ANALOG),
        'Y': ((uinput.KEY_S, uinput.KEY_W), FALSE_ANALOG),
        'RX': (uinput.ABS_RX, ANALOG),
        'RY': (uinput.ABS_RY, ANALOG),
        'para': (uinput.KEY_SPACE, BUTTON),
        'graf': (uinput.KEY_LEFTCTRL, BUTTON),
        'fuck': (uinput.BTN_0, BUTTON),
        'yeah': (uinput.BTN_2, BUTTON),
        'walk': (uinput.KEY_W, BUTTON),
        '_': (uinput.BTN_JOYSTICK, BUTTON)
    }

    def __init__(self, actions=DEFAULT_ACTIONS_JOYSTICK, name='Gamepad'):
        self.actions = actions

        uinput_events = []
        for a, t in actions.values():
            if t in (Joystick.BUTTON, Joystick.MOUSE):
                uinput_events.append(a)
            if t == Joystick.ANALOG:
                uinput_events.append(a + Joystick.ANALOG_RANGE)
            elif t == Joystick.FALSE_ANALOG:
                uinput_events.extend(a)

        self.device = uinput.Device(uinput_events, name)

        self.parachute_opening = False
        self.last_gesture = Glove.FINGER_POSITIONS['OPEN']
        self.last_time_pressed = 0
        self.last_time_changed = 0
        self.ready_to_graffiti = False

    def update(self, direction, fingers):
        self.update_joystick(direction)
        self.update_buttons(fingers)

    def update_joystick(self, direction):
        x, y = direction
        for k, v in zip(["X", "Y", "RX"], [x, -y, int(RX_FACTOR * x)]):
            self.emit(k, v)

    def update_buttons(self, fingers):
        if fingers == self.last_gesture:
            if self.check_last_changed() and self.check_last_pressed():
                self.emit_from_fingers(fingers)
        else:
            self.last_time_changed = self.get_time()
            self.last_gesture = fingers
            self.parachute_opening = False
            if fingers != Glove.FINGER_POSITIONS['FIST']:
                self.ready_to_graffiti = False

    def emit_from_fingers(self, fingers):
        if fingers == Glove.FINGER_POSITIONS['FUCK']:
            self.emit('fuck', 1)
        elif fingers == Glove.FINGER_POSITIONS['YEAH']:
            self.emit('yeah', 1)
        elif fingers == Glove.FINGER_POSITIONS['GRAF']:
            self.ready_to_graffiti = True
        elif fingers == Glove.FINGER_POSITIONS['FIST']:
            if self.ready_to_graffiti:
                self.emit('graf', 1)
                self.ready_to_graffiti = False
        self.last_time_pressed = self.get_time()

    def open_parachute(self):
        self.emit('para', 1)

    def walk(self, fingers):
        if self.last_gesture == Glove.FINGER_POSITIONS['OPEN']:
            self.device.emit(uinput.KEY_W, 1)
        if fingers == Glove.FINGER_POSITIONS['OPEN']:
            self.device.emit(uinput.KEY_W, 0)
            self.last_time_changed = self.get_time()
        self.last_gesture = fingers

    def is_walking(self):
        return self.last_gesture != Glove.FINGER_POSITIONS['OPEN']

    def reset(self):
        for action in self.actions:
            self.emit(action, 0, False)
        self.device.syn()

    def emit(self, k, v, syn=True):
        if k not in self.actions:
            return
        elif self.actions[k][1] in (Joystick.ANALOG, Joystick.MOUSE):
            self.device.emit(self.actions[k][0], v, syn)
        elif self.actions[k][1] == Joystick.BUTTON and v != 0:
            self.device.emit_click(self.actions[k][0], syn)
        elif self.actions[k][1] == Joystick.FALSE_ANALOG:
            ks = self.actions[k][0]
            if k == "X":
                vs = [1 if v < -X_THRESH else 0, 1 if v > X_THRESH else 0]
            else:
                vs = [1 if v < -Y_THRESH else 0, 1 if v > Y_THRESH else 0]
            for i in (0, 1):
                self.device.emit(ks[i], vs[i], False)

    def is_parachute_opening(self):
        return self.parachute_opening

    def check_last_pressed(self):
        if self.last_time_pressed < self.last_time_changed:
            return True
        else:
            return self.get_time() - self.last_time_pressed > self.MIN_REPRESS_TIME

    def check_last_changed(self):
        return self.get_time() - self.last_time_changed > self.MIN_PRESS_TIME

    @staticmethod
    def get_time():
        return int(round(time.time() * 1000))
