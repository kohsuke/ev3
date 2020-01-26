# access joystick
import os
import pygame
import time

pygame.init()
pygame.joystick.init()

j = pygame.joystick.Joystick(0)
j.init()


while True:
    pygame.event.pump()
    os.system("clear")
    print("%s axis=%d"%(j.get_name(),j.get_numaxes()))
    for i in range(j.get_numaxes()):
        print("%+0.2f"%(j.get_axis(i)))
    time.sleep(0.1)