#!/usr/bin/python

import os
import sys
import math
import random

from time import sleep, time
from hippietrap.chandelier import Chandelier, BROADCAST, NUM_NODES
from hippietrap.color import Color

device = "/dev/serial0"

ch = Chandelier()
ch.open(device)
ch.off(BROADCAST)

start = int(sys.argv[1])

for id in range(start,NUM_NODES+1):
    ch.set_color(id, Color(0,0,0))

for id in range(start,NUM_NODES+1):
    print id
    ch.set_color(id, Color(0,0,255))
    sleep(.25)