from ev3 import EV3Cmds
import binascii

c=EV3Cmds()
c.sound.tone(volume=100, frequency=440, duration=1000)
print(binascii.hexlify(c.encode()))