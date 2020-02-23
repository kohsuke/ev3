# access joystick
import os
import pygame
import time

pygame.init()
pygame.joystick.init()

j = pygame.joystick.Joystick(0)
j.init()

print(j.get_name())

while True:
    pygame.event.pump()
    print(" axis=%d"%(j.get_numaxes()), end="")
    for i in range(j.get_numaxes()):
        print(" %+0.2f"%(j.get_axis(i)), end="")

    print(" buttons=%d"%(j.get_numbuttons()), end="")
    for i in range(j.get_numbuttons()):
        print(" %d"%(j.get_button(i)), end="")
    print(end="\r")
    time.sleep(0.1)