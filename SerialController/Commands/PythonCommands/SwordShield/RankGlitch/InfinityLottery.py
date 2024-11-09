#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Commands.Keys import Button, Direction
from Commands.PythonCommandBase import PythonCommand


# using Rank Battle glitch
# Infinity ID lottery
# 無限IDくじ(ランクマッチ使用)
class InfinityLottery(PythonCommand):
    NAME = '【剣盾】無限IDくじ'

    def __init__(self):
        super().__init__()

    def do(self):
        while True:
            self.press(Button.A, wait=0.5)
            self.press(Button.B, wait=0.5)
            self.press(Direction.DOWN, wait=0.5)

            for _ in range(0, 10):  # A loop
                self.press(Button.A, wait=0.5)

            for _ in range(0, 20):  # B loop
                self.press(Button.B, wait=0.5)

            # Time glitch
            self.timeLeap()
