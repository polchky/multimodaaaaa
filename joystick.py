import uinput


class Joystick:
    ANALOG = 0
    BUTTON = 1
    DEFAULT_ACTIONS = {
        'X': (uinput.ABS_X, ANALOG),
        'Y': (uinput.ABS_Y, ANALOG),
        'RX': (uinput.ABS_RX, ANALOG),
        'RY': (uinput.ABS_RY, ANALOG),
        'para': (uinput.BTN_0, BUTTON),
        'graf': (uinput.BTN_1, BUTTON),
        'fuck': (uinput.BTN_2, BUTTON),
        'yeah': (uinput.BTN_3, BUTTON)
    }

    def __init__(self, actions=DEFAULT_ACTIONS, name='Gamepad'):
        self.actions = actions
        self.state = dict.fromkeys(actions, 0)
        self.device = uinput.Device([a[0] for a in actions.values()], name)

    def update(self, actions):
        for k in actions:
            self.emit(k, actions[k])
        self.device.syn()

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