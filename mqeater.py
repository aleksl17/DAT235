from sense_emu import SenseHat
from time import sleep
import sys
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import time
import Logger

sense = SenseHat()
x_pos = 0
y_pos = 7
white = (255, 255, 255)
trail = (0, 0, 0)
eater = (255, 255, 0)
visited = None
ipConnect = "localhost"
startload = "Write 'ordered' to start\n"

print(startload)

publish.single("dat235/groupnine/joystick", payload=None, qos=0, hostname=ipConnect)
publish.single("dat235/groupnine/start", startload, retain=True, qos=1, hostname=ipConnect)

log = Logger.Logger("MQEater_event.log","Logging a PixelEater run")


def allEaten():
    global visited
    accum = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if visited[x][y]:
                accum += 1

    return accum == 64

def matrix_init():
    global visited
    global x_pos
    global y_pos
    visited = [[False for i in range(0, 8)] for j in range(0, 8)]
    x_pos = 0
    y_pos = 7
    sense.clear(white)
    sense.set_pixel(x_pos, y_pos, eater)
    visited[x_pos][y_pos] = True
    log.log_pixel(x_pos,y_pos,eater)


def event_loop():
    global x_pos
    global y_pos
    while True:   
        order = subscribe.simple("dat235/groupnine/start", hostname=ipConnect)     
        msg = subscribe.simple("dat235/groupnine/joystick/#", hostname=ipConnect)
        print(msg)
        print(order)

        if msg.topic == "dat235/groupnine/joystick/up":
            sense.set_pixel(x_pos, y_pos, trail)
            y_pos = (y_pos - 1) % 8
            sense.set_pixel(x_pos, y_pos, eater)
            visited[x_pos][y_pos] = True
            log.log_joystick("up")
        if msg.topic == "dat235/groupnine/joystick/down":
            sense.set_pixel(x_pos, y_pos, trail)
            y_pos = (y_pos + 1) % 8
            sense.set_pixel(x_pos, y_pos, eater)
            visited[x_pos][y_pos] = True
            log.log_joystick("down")
        if msg.topic == "dat235/groupnine/joystick/left":
            sense.set_pixel(x_pos, y_pos, trail)
            x_pos = (x_pos - 1) % 8
            sense.set_pixel(x_pos, y_pos, eater)
            visited[x_pos][y_pos] = True
            log.log_joystick("left")
        if msg.topic == "dat235/groupnine/joystick/right":
            sense.set_pixel(x_pos, y_pos, trail)
            x_pos = (x_pos + 1) % 8
            sense.set_pixel(x_pos, y_pos, eater)
            visited[x_pos][y_pos] = True
            log.log_joystick("right")
        if allEaten():
            print("All eaten")
            break
            #sleep(1)
            #sense.clear()
            #sys.exit(0)
        if order == "ordered":                                          #start
            matrix_init()
        # ~ if combined == 'heldmiddle':                                #stop
            # ~ sense.show_message('Exit')
            # ~ sense.clear()
            # ~ sleep(1)
            # ~ sys.exit(0)


if __name__ == '__main__':
    log.log_time(time.time(),"MQ Pixel Eater Log Started") 
    matrix_init()
    event_loop()
    log.StopLog("Done Logging")
    print("Main Exited")
