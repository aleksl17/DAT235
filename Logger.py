import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import time
import json

ipConnect = "10.0.0.201"

EV_Joystick     = "Joystick"
EV_Time         = "Time"
EV_Clear        = "Clear"
EV_Pixel        = "Pixel"
EV_Pixelmap     = "Pixelmap"
EV_Message      = "Message"
EV_Letter       = "Letter"


class Logger:
    f = None
    
    def __init__(self, filename = "MQEater_event.log", message=""):
        self.f = open(filename,"w")
        self.f.write("#\n")
        self.f.write("#  Sense HAT logging started: "+time.asctime()+" "+message+"\n")
        self.f.write("#\n")

    def _write(self, event : str):
        self.f.write("@"+event+"\n")

    def log_joystick(self, event):
        """Logging a Sense HAT Joystick event"""
        event = [EV_Joystick, event]
        self._write(json.dumps(event))
        
    def log_time(self, timestamp=None,message=""):
        """Logging a Sense HAT time event"""
        if timestamp==None:
            timestamp = time.time()
        event = [EV_Time, timestamp]
        if message!="":
            event.append(message)
        self._write(json.dumps(event))
    
    def log_clear(self, rgb=[0,0,0]):
        """Log a call to clear()"""
        event = [EV_Clear, rgb]
        self._write(json.dumps(event))

    def log_pixel(self, x,y,rgb):
        """Log a pixel setting"""
        event = [EV_Pixel, x, y, rgb]
        self._write(json.dumps(event))

    def log_pixelmap(self, pixelmap):
        """Log a pixel map"""
        event = [EV_Pixelmap, pixelmap]
        self._write(json.dumps(event))
    
    def log_message(self, message, scroll_speed, text_colour, back_colour):
        """Log show_message"""
        event = [EV_Message, message, scroll_speed, text_colour, back_colour]
        self._write(json.dumps(event))
    
    def log_letter(self, char, text_colour, back_colour):
        """Log show_message"""
        event = [EV_Letter, char, text_colour, back_colour]
        self._write(json.dumps(event))
    
    def log_temperature(self, temperature):
        """Log temperature"""
        event = [EV_Temperature, temperature]
        self._write(json.dumps(event))
    
    def StopLog(self, message=""):
        """Close the log"""
        self.f.write("#\n")
        self.f.write("#  Sense HAT logging stopped: "+time.asctime()+" "+message+"\n")
        self.f.write("#\n")
        self.f.close()


log = Logger("MQEater.log", "Logging PixelEater run")
#logSub = subscribe.simple("dat235/groupnine/start", hostname=ipConnect)
#joySub = subscribe.simple("dat235/groupnine/start", hostname=ipConnect)
logWhile = True


if __name__ == "__main__":
    log.log_time(time.time(), "PixelEater Log Started")

    while logWhile:
        logSub = subscribe.simple("dat235/groupnine/start/#", hostname=ipConnect)
        joySub = subscribe.simple("dat235/groupnine/joystick/#", hostname=ipConnect)
        print(joySub)
        print(joySub.topic)
        print(logSub.topic)

        if joySub.topic == "dat235/groupnine/joystick/up":
            log.log_joystick("up")
        if joySub.topic == "dat235/groupnine/joystick/down":
            log.log_joystick("down")
        if joySub.topic == "dat235/groupnine/joystick/left":
            log.log_joystick("left")
        if joySub.topic == "dat235/groupnine/joystick/right":
            log.log_joystick("right")

        if joySub.topic == "dat235/groupnine/joystick/stoplog":
            log.StopLog("Done Logging")
            logWhile = False


    print("Main Done")


