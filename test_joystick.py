import time
from joystick import Joystick

g = Joystick(name='Test_Gamepad')

analogs = [x for x in g.actions if g.actions[x][1] == Joystick.ANALOG]
buttons = [x for x in g.actions if g.actions[x][1] == Joystick.BUTTON]

print("Press ENTER to begin test")
raw_input()

for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

print("Testing analog actions:")
for a in analogs:
    print(a)
    for i in range(0, 256, 4):
        g.update({a: i})
        time.sleep(0.02)

for b in buttons:
    print(b)
    g.update({b: 1})
    time.sleep(0.5)

for b in buttons:
    for c in buttons:
        if c != b:
            print(b + " + " + c)
            g.update({b: 1, c: 1})
            time.sleep(0.5)

print("Reset")
g.reset()
print("Done!")