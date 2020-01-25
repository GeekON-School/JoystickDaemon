import time
import pygame
import pyautogui
from pygame import locals


def main():
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for j in joysticks:
        j.init()
        print(j.get_name())
        print("  Balls: {}".format(j.get_numballs()))
        print("  Axes: {}".format(j.get_numaxes()))
        print("  Hats: {}".format(j.get_numhats()))
        print("  Buttons: {}".format(j.get_numbuttons()))

    while True:
        for e in pygame.event.get():  # iterate over event stack
            if e.type == pygame.locals.JOYBUTTONDOWN:
                print("KeyDown:")
                for jid, j in enumerate(joysticks):
                    for bid in range(j.get_numbuttons()):
                        if j.get_button(bid):
                            print("  Joystick {}, Button {}".format(jid, bid))
        time.sleep(0.5)


if __name__ == '__main__':
    main()
