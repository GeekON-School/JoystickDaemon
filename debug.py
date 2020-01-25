import pygame
import pyautogui


def main():
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for j in joysticks:
        j.init()
        print(j.get_name())
        print("  Balls:", j.get_numballs())
        print("  Axes:", j.get_numaxes())
        print("  Hats:", j.get_numhats())
        print("  Buttons:", j.get_numbuttons())


if __name__ == '__main__':
    main()
