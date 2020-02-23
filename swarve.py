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

# represents control parameters for different motors
class Motor:
    def __init__(self, layer, no, p):
        self.layer = layer
        self.no    = no         # motor ID in [0,3]
        self.mask  = 1<<no      # motor bitmask
        self.polarity = p       # polarity direction, +1 or -1

pygame.init()
pygame.joystick.init()

j = pygame.joystick.Joystick(0)
j.init()

# gear ratio for the directional motor, in the reverse order
# so as to map the turrent angle to the tacho count
g = Gear(Gear.TURRET, Gear.BIG)

motors = [Motor(0,0,1), Motor(0,2,-1)]

# Open EV3 as device
with hid.Device(0x0694,5) as ev3:
    # reset tacho counts on all motors
    c = Program()
    c.output.reset(15).clear_count(15)
    for m in motors:
        c.output.ports(m.mask).power(0).polarity(m.polarity).start()
    c.send(ev3)
    print("Initialized")

    loop = 0            # loop counter, just to assist debugging
    t = 0               # target direction

    # Main game loop
    while True:
        time.sleep(0.1)
        pygame.event.pump()

        # read the target direction from joystick
        t = target(j) or t
        print("l:%5d t:%+3.2f" % (loop, t), end="")

        # read current tacho meter for motors
        c = Program()
        for m in motors:
            m.tacho = c.globalVar(4)
            c.output.get_count(m.no, m.tacho, layer=m.layer)
        c.send(ev3)


        # determine the power level for each motor to get to the target
        c = Program()
        for m in motors:
            current = g(m.tacho())*m.polarity

            d = delta(t,current)

            # convert that delta to power level
            #  - clamp at the threshold to control the maximum
            #  - to avoid jitter, power down motor near the target position
            threshold = 80
            if abs(d)>threshold:    d=math.copysign(threshold,d)
            if abs(d)<3:            d=0
            d = int(d)

            c.output.power(d, ports=m.mask, layer=m.layer)

            print(" c:%+3.2f d:%+3.2f" % (current, d), end="")


        # apply power accordingly
        c.send(ev3)

        loop += 1
        print()

