import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
# from sense_emu import SenseHat
import time
import sys
import json
import Logger

# sense = SenseHat()

ipConnect = "localhost"

if len(sys.argv) == 1:
    log_name = input("Which log file to read? ")
else:
    log_name = sys.argv[1]

try:
    f = open(log_name, "r")
except:
    sys.stderr.write("Well, that didn't go so well. Just couldn't open the file '" + log_name + "'")
    sys.exit(1)

simtime = None

for line in f:
    if line[0] == "@":
        event = json.loads(line[1:])
        print("Event: ", event[0], event[1])
        time.sleep(1)
        if event[0] == Logger.EV_Joystick:
            if event[1] == "up":
                publish.single("dat235/groupnine/joystick/up", hostname=ipConnect)
            if event[1] == "down":
                publish.single("dat235/groupnine/joystick/down", hostname=ipConnect)
            if event[1] == "left":
                publish.single("dat235/groupnine/joystick/left", hostname=ipConnect)
            if event[1] == "right":
                publish.single("dat235/groupnine/joystick/right", hostname=ipConnect)

# ~ print(json.loads(line[0]))

# ~ for line in f:
# ~ if line[0]=="@":
# ~ event = json.loads(line[1:])
# ~ #nxtEvent = json.loads(line[1:])
# ~ print("Event: ",event[0],end=" - ")
# ~ #print("Next Event: ",nxtEvent[0],end=" - ")

# ~ if event[0] == Logger.EV_Pixel:
# ~ startXPos = event[1]
# ~ startYPos = event[2]


# ~ for line in f:
# ~ if line[0]=="@":
# ~ event = json.loads(line[1:])
# ~ print("Event: ",event[0],end=" - ")
# ~ print(event[1], ",", event[2])
# ~ if event[0] == Logger.EV_Pixel:
# ~ startXPos = event[1]
# ~ startYPos = event[2]
