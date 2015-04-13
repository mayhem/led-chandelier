#!/usr/bin/python

import serial
import struct
from time import sleep

BAUD_RATE = 38400

def crc16_update(crc, a):
    crc ^= a
    for i in xrange(0, 8):
        if crc & 1:
            crc = (crc >> 1) ^ 0xA001
        else:
            crc = (crc >> 1)
    return crc

class Chandelier(object):

    def __init__(self):
        self.ser = None

    def open(self, device):

        try:
            print "Opening %s" % device
            self.ser = serial.Serial(device, 
                                     BAUD_RATE, 
                                     bytesize=serial.EIGHTBITS, 
                                     parity=serial.PARITY_NONE, 
                                     stopbits=serial.STOPBITS_ONE,
                                     timeout=.01)
        except serial.serialutil.SerialException, e:
            print "Cant open serial port: %s" % device
            sys.exit(-1)

    def set_color(self, red, green, blue):
        packet = chr(red) + chr(green) + chr(blue);
        crc = 0
        for ch in packet:
            crc = crc16_update(crc, ord(ch))
        packet = struct.pack("<BB", 255,  len(packet) + 2) + packet + struct.pack("<H", crc)
        self.ser.write(packet)

def color_wheel(wheel_pos):
    color = [0,0,0]
    wheel_pos = 255 - wheel_pos
    if wheel_pos < 85:
        color[0] = int(255 - wheel_pos * 3)
        color[1] = 0
        color[2] = int(wheel_pos * 3)
    elif wheel_pos < 170:
        wheel_pos -= 85
        color[0] = 0
        color[1] = int(wheel_pos * 3)
        color[2] = 255 - int(wheel_pos * 3)
    else:
        wheel_pos -= 170
        color[0] = int(wheel_pos * 3)
        color[1] = 255 - int(wheel_pos * 3)
        color[2] = 0

    return color

ch = Chandelier()
ch.open("/dev/ttyAMA0")

while True:
    for i in xrange(256 * 6):
        col = color_wheel(i & 255)
        ch.set_color(col[0], col[1], col[2])
        sleep(.02)
