#!/usr/bin/env python

import os
import sys
import math
from random import random, randint
from hippietrap.hippietrap import HippieTrap, ALL, NUM_NODES
from hippietrap.pattern import PatternBase, run_pattern
from hippietrap.color import hue_to_color
from time import sleep, time

class Sparkle(PatternBase):

    def pattern(self):

        trap.start_pattern(ALL)
        while True:
            for i in range(15):
                bottle = randint(1, NUM_NODES)
                led = randint(1, 4)
                trap.set_color(bottle, hue_to_color(random()))

            trap.send_decay(ALL, 4)
            sleep(.3)

            if self.stop_thread:
                return

if __name__ == "__main__":
    with HippieTrap() as trap:
        trap.begin()
        run_pattern(trap, Sparkle)
        trap.clear(ALL)