from ev3 import EV3Cmds
import binascii

import hid
with hid.Device(0x0694,5) as h:
    c = EV3Cmds()
    c.sound.tone(volume=1, frequency=440, duration=100)
    c.sound.ready()

    # c.output.ports(0xF).speed(10).start()
    # c.output.stop(ports=0xF)

    # c.output.layer(0).ports(0xF).speed(10).start()
    # c.output.layer(1).ports(0xF).speed(10).start()

    c.output.stop(ports=0xF).layer(1).stop(ports=0x0F)

    # c.sound.tone(volume=1, frequency=550, duration=100)
    # c.sound.ready()
    # c.sound.tone(volume=1, frequency=660, duration=100)
    # c.sound.ready()

    c.ui.led(color='orange',mode='off')

    print(binascii.hexlify(c.encode()))
    c.send(h)


