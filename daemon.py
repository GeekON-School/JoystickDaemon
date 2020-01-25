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
        self.last_active = 0  # time.monotonic()
        self.key = key

    def update(self, event):
        value = self.joystick.get_axis(self.axis)
        if (self.positive and value > TILT_THRESHOLD) or (not self.positive and value < -TILT_THRESHOLD):
            self.last_active = time.monotonic()
            if not self.pressed:
                pyautogui.keyDown(self.key)
                self.pressed = True
        else:
            if time.monotonic() - self.last_active > RELEASE_DELAY:
                if self.pressed:
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

    for joystick_config in config:
        joystick = pygame.joystick.Joystick(joystick_config['id'])
        for axis_config in joystick_config['axes']:
            if 'positive' in axis_config:
                buttons.append(AxisKey(joystick, axis_config['id'], True, axis_config['positive']))
            if 'negative' in axis_config:
                buttons.append(AxisKey(joystick, axis_config['id'], False, axis_config['negative']))
        for button_config in joystick_config['buttons']:
            buttons.append(ButtonKey(joystick, button_config['id'], button_config['key']))

    while True:
        for e in pygame.event.get():
            for button in buttons:
                button.update(e.type)
        time.sleep(0.01)


if __name__ == '__main__':
    main()
