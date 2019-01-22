import pygame
import pyautogui
import time
from pygame import locals

AXIS_X = 0
AXIS_Y = 3
BUTTON_A = 0  # E
BUTTON_B = 1  # space
BUTTON_C = 2  # R
BUTTON_D = 3  # Q
BUTTON_E = 4  # F
BUTTON_F = 5  # Z
HOLD_TIME = 120

buttons = {BUTTON_A: False, BUTTON_B: False, BUTTON_C: False, BUTTON_D: False, BUTTON_E: False, BUTTON_F: False}
wasd = {"w": [0, False], "a": [0, False], "s": [0, False], "d": [0, False]}


def process_wasd():
    global wasd
    for k in wasd:
        if wasd[k][1] and int(round(time.time() * 1000)) - wasd[k][0] >= HOLD_TIME:
            wasd[k][1] = False
            pyautogui.keyUp(k)
        elif not wasd[k][1] and int(round(time.time() * 1000)) - wasd[k][0] < HOLD_TIME:
            wasd[k][1] = True
            pyautogui.keyDown(k)


def loophandler(joy):
    global buttons
    while 1:
        for e in pygame.event.get():  # iterate over event stack
            if e.type == pygame.locals.JOYAXISMOTION:
                x, y = joy.get_axis(0), joy.get_axis(AXIS_Y)
                if x < -0.5:  # Left
                    wasd["a"][0] = int(round(time.time() * 1000))
                elif x > 0.5:  # Right
                    wasd["d"][0] = int(round(time.time() * 1000))
                if y > 0.5:  # Down (yes, it's weird)
                    wasd["s"][0] = int(round(time.time() * 1000))
                elif y < -0.5:  # Up (yes, it's weird)
                    wasd["w"][0] = int(round(time.time() * 1000))
                process_wasd()
            elif e.type == pygame.locals.JOYBUTTONDOWN:
                if not buttons[BUTTON_A] and joy.get_button(BUTTON_A):
                    buttons[BUTTON_A] = True
                    pyautogui.keyDown('e')
                if not buttons[BUTTON_B] and joy.get_button(BUTTON_B):
                    buttons[BUTTON_B] = True
                    pyautogui.keyDown('space')  # todo
                if not buttons[BUTTON_C] and joy.get_button(BUTTON_C):
                    buttons[BUTTON_C] = True
                    pyautogui.keyDown('r')  # todo
                if not buttons[BUTTON_D] and joy.get_button(BUTTON_D):
                    buttons[BUTTON_D] = True
                    pyautogui.keyDown('q')  # todo
                if not buttons[BUTTON_E] and joy.get_button(BUTTON_E):
                    buttons[BUTTON_E] = True
                    pyautogui.keyDown('f')  # todo
                if not buttons[BUTTON_F] and joy.get_button(BUTTON_F):
                    buttons[BUTTON_F] = True
                    pyautogui.keyDown('z')  # todo
            elif e.type == pygame.locals.JOYBUTTONUP:
                if buttons[BUTTON_A] and not joy.get_button(BUTTON_A):
                    buttons[BUTTON_A] = False
                    pyautogui.keyUp('e')
                if buttons[BUTTON_B] and not joy.get_button(BUTTON_B):
                    buttons[BUTTON_B] = False
                    pyautogui.keyUp('space')  # todo
                if buttons[BUTTON_C] and not joy.get_button(BUTTON_C):
                    buttons[BUTTON_C] = False
                    pyautogui.keyUp('r')  # todo
                if buttons[BUTTON_D] and not joy.get_button(BUTTON_D):
                    buttons[BUTTON_D] = False
                    pyautogui.keyUp('q')  # todo
                if buttons[BUTTON_E] and not joy.get_button(BUTTON_E):
                    buttons[BUTTON_E] = False
                    pyautogui.keyUp('f')  # todo
                if buttons[BUTTON_F] and not joy.get_button(BUTTON_F):
                    buttons[BUTTON_F] = False
                    pyautogui.keyUp('z')  # todo


if __name__ == '__main__':
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print(joysticks)

    try:
        j = pygame.joystick.Joystick(0)  # create a joystick instance
        j.init()  # init instance
        print('Enabled joystick: ' + j.get_name())
        loophandler(j)
    except pygame.error:
        print('No joystick found. Terminated.')
        exit()
