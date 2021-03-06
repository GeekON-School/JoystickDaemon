import sys
import json
import time

import pygame
import pyautogui
from pygame import locals


TILT_THRESHOLD = 0.5
RELEASE_DELAY = 0.05


class ButtonKey:
    def __init__(self, joystick, button, key):
        self.joystick = joystick
        self.button = button
        self.pressed = False
        self.key = key

    def update(self, event):
        if event == pygame.locals.JOYBUTTONDOWN:
            if self.joystick.get_button(self.button) and not self.pressed:
                pyautogui.keyDown(self.key)
                self.pressed = True
        elif event == pygame.locals.JOYBUTTONUP:
            if not self.joystick.get_button(self.button) and self.pressed:
                self.pressed = False
                pyautogui.keyUp(self.key)


class AxisKey:
    def __init__(self, joystick, axis, positive, key):
        self.joystick = joystick
        self.axis = axis
        self.positive = positive
        self.pressed = False
        self.last_active = 0  # time.time()
        self.key = key

    def update(self):
        value = self.joystick.get_axis(self.axis)
        if (self.positive and value > TILT_THRESHOLD) or (not self.positive and value < -TILT_THRESHOLD):
            self.last_active = time.time()
            if not self.pressed:
                pyautogui.keyDown(self.key)
                self.pressed = True
        else:
            if self.pressed and time.time() - self.last_active > RELEASE_DELAY:
                self.pressed = False
                pyautogui.keyUp(self.key)


def main():
    config_path = "configs/default.json"
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    with open(config_path, 'r') as f:
        config = json.load(f)

    pygame.init()
    print("Joysticks: {}".format(pygame.joystick.get_count()))

    buttons = []
    axes = []

    for joystick_config in config:
        joystick = pygame.joystick.Joystick(joystick_config['id'])
        if not joystick.get_init():
            joystick.init()
        for axis_config in joystick_config['axes']:
            if 'positive' in axis_config:
                axes.append(AxisKey(joystick, axis_config['id'], True, axis_config['positive']))
            if 'negative' in axis_config:
                axes.append(AxisKey(joystick, axis_config['id'], False, axis_config['negative']))
        for button_config in joystick_config['buttons']:
            buttons.append(ButtonKey(joystick, button_config['id'], button_config['key']))

    while True:
        for e in pygame.event.get():
            if e.type in [pygame.locals.JOYBUTTONDOWN, pygame.locals.JOYBUTTONUP]:
                for button in buttons:
                    button.update(e.type)
            elif e.type == pygame.locals.JOYAXISMOTION:
                for axis in axes:
                    axis.update()
        time.sleep(0.01)


if __name__ == '__main__':
    main()
