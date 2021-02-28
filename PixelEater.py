# Python bytecode 3.5 (3351)
# Embedded file name: ./PixelEater.py
# Compiled at: 2018-08-29 20:32:46
# Size of source mod 2**32: 2760 bytes
# Decompiled by https://python-decompiler.com
from sense_emu import SenseHat
from time import sleep
import sys
sense = SenseHat()
x_pos = 0
y_pos = 7
cix = 0
red = (127, 0, 0)
green = (0, 127, 0)
blue = (0, 0, 127)
white = (127, 127, 127)
yellow = (127, 127, 0)
black = (0, 0, 0)
trail = black
eater = (255, 255, 0)
visited = None
afewcolors = (
 red, green, blue, white, yellow)

def allEaten():
    global visited
    accum = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if visited[x][y]:
                accum += 1

    return accum == 64


def matrix_init():
    global cix
    global visited
    global x_pos
    global y_pos
    visited = [[False for i in range(0, 8)] for j in range(0, 8)]
    x_pos = 0
    y_pos = 7
    sense.clear(afewcolors[cix])
    cix = (cix + 1) % len(afewcolors)
    sense.set_pixel(x_pos, y_pos, eater)
    visited[x_pos][y_pos] = True


def event_loop():
    global x_pos
    global y_pos
    while True:
        for event in sense.stick.get_events():
            action = event.action
            direction = event.direction
            combined = action + direction
            if combined in ('heldup', 'pressedup'):
                sense.set_pixel(x_pos, y_pos, trail)
                y_pos = (y_pos - 1) % 8
                sense.set_pixel(x_pos, y_pos, eater)
                visited[x_pos][y_pos] = True
            if combined in ('helddown', 'presseddown'):
                sense.set_pixel(x_pos, y_pos, trail)
                y_pos = (y_pos + 1) % 8
                sense.set_pixel(x_pos, y_pos, eater)
                visited[x_pos][y_pos] = True
            if combined in ('pressedleft', 'heldleft'):
                sense.set_pixel(x_pos, y_pos, trail)
                x_pos = (x_pos - 1) % 8
                sense.set_pixel(x_pos, y_pos, eater)
                visited[x_pos][y_pos] = True
            if combined in ('pressedright', 'heldright'):
                sense.set_pixel(x_pos, y_pos, trail)
                x_pos = (x_pos + 1) % 8
                sense.set_pixel(x_pos, y_pos, eater)
                visited[x_pos][y_pos] = True
            if allEaten():
                sense.show_message('Game Completed')
                sleep(1)
                sense.clear()
                sys.exit(0)
            if combined == 'pressedmiddle':
                matrix_init()
            if combined == 'heldmiddle':
                sense.show_message('Exit')
                sense.clear()
                sleep(1)
                sys.exit(0)


if __name__ == '__main__':
    matrix_init()
    event_loop()
