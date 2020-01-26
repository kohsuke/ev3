from ev3 import EV3Cmds
import binascii

import hid
with hid.Device(0x0694,5) as h:
    c = EV3Cmds()
    c.sound.tone(volume=1, frequency=440, duration=100)
    c.sound.ready()
    c.sound.tone(volume=1, frequency=550, duration=100)
    c.sound.ready()
    c.sound.tone(volume=1, frequency=660, duration=100)
    c.sound.ready()

    print(binascii.hexlify(c.encode()))
    c.send(h)


