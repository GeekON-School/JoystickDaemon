import pygame
import pyautogui


def main():
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print(joysticks)


if __name__ == '__main__':
    main()
