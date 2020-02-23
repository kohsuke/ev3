# Map analog stick to a 360 direction
# 0 is to the right
import math
import pygame
import time
from ev3 import Program
from gear import Gear
import hid

def delta(target, current):
    # calculate delta, which is the angle we need to travel
    # TODO: make this modulo 180 to reduce travel distance in case of a large direction change
    # this requires switching the polarity of the motor
    delta = (target - current) % 360
    # normalize negative to positive, then we'll separately figure out whether it's best to
    # go clockwise or counter-clockwise
    delta = (delta + 360) % 360
    if delta > 180:
        delta = delta - 360
    return delta


def target(j):
    """
    Read the target angle from joystick in [-180,180],
    or None if no input is given
    """

    x = j.get_axis(0)
    y = -j.get_axis(1)  # y increases from top to bottom, which is the opposite direction of typical math

    # if the analog stick isn't pressed enough distance, ignore
    if math.hypot(x, y) < 0.7:
        return None

    # compute that target angle in degree
    return math.atan2(y, x) * 180 / math.pi


pygame.init()
pygame.joystick.init()

j = pygame.joystick.Joystick(0)
j.init()

# gear ratio for the directional motor, in the reverse order
# so as to map the turrent angle to the tacho count
g = Gear(Gear.TURRET, Gear.BIG)

# Open EV3 as device
with hid.Device(0x0694,5) as ev3:
    # reset tacho counts on all motors
    c = Program()
    c.output.reset(15).clear_count(15)
    # c.output.ports(1).power(0).start()
    c.send(ev3)
    print("Initialized")

    loop = 0

    # Main game loop
    while True:
        time.sleep(0.1)
        pygame.event.pump()

        # read current tacho meter
        c = Program()
        tacho = c.globalVar(4)
        c.output.get_count(0, tacho)
        c.send(ev3)

        current = g(tacho())

        t = target(j) or current

        d = delta(t,current)

        print("l:%5d t:%+3.2f c:%+3.2f d:%+3.2f" % (loop,t,current,d))

        # convert that delta to power level
        #  - clamp at the threshold to control the maximum
        #  - to avoid jitter, power down motor near the target position
        threshold = 80
        if abs(d)>threshold:    d=math.copysign(threshold,d)
        if abs(d)<3:            d=0
        d = int(d)

        # apply power accordingly
        c = Program()
        c.output.ports(1)
        c.output.power(d)
        c.send(ev3)

        loop += 1


