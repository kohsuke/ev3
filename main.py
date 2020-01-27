from ev3 import Program
from gear import Gear
import binascii
import time
import hid


with hid.Device(0x0694,5) as h:
    c = Program()
    c.sound.tone(volume=1, frequency=440, duration=100)
    c.sound.ready()

    # c.output.ports(0xF).speed(10).start()
    # c.output.stop(ports=0xF)

    # c.output.layer(0).ports(0xF).speed(10).start()
    # c.output.layer(1).ports(0xF).speed(10).start()

    # c.output.stop(ports=0xF).layer(1).stop(ports=0x0F)

    # c.sound.tone(volume=1, frequency=550, duration=100)
    # c.sound.ready()
    # c.sound.tone(volume=1, frequency=660, duration=100)
    # c.sound.ready()

    c.ui.led(color='orange',mode='off')

    g = Gear(Gear.BIG,Gear.TURRET)

    c.output.ports(2)
    # c.output.polarity(1)

    # move_by_X functions seem to internally reset tacho count
    # so read is not giving me meaningful tacho count
    c.output.move_by_step( g(60), g(240), g(60), speed=20)
    # c.output.ready()
    # c.output.move_by_step( g(60), g(240), g(60), speed= 20)

    c.send(h)

    for i in range(50):
        c = Program()
        speed = c.globalVar(1)
        tacho = c.globalVar(4)
        c.output.read(1, speed, tacho)
        # print(binascii.hexlify(c.encode()))
        c.send(h)
        print("speed:%d tacho:%d"%(speed(),tacho()))
        time.sleep(0.1)



