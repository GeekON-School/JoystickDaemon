import pygame
import pyautogui
import time


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
        for i, j in enumerate(joysticks):
            print("j{} ".format(i) + "".join("{: 3}".format('#' if j.get_button(x) else 'O')
                                             for x in range(j.get_numbuttons())))
            print("   " + "".join("{: 3}".format(x) for x in range(j.get_numbuttons())))
        time.sleep(1)


if __name__ == '__main__':
    main()
