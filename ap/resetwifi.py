import RPi.GPIO as GPIO
import time;
import os

from shutil import copyfile

from threading import Timer

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) 



source = "source.txt"
target = "target.txt"

def setupHOTSPOT():
    os.system ("./makehotspot shroomkeeper ShroomKeeper")
    global source
    global target
    copyfile(source,target)


rt = None

def callback_timer(message):
    print(message);
    val=  GPIO.input(26)
    global rt
    rt.stop()
    rt = None
    if val == 0:
        print("user pressed the reset HOTSPOT button for 5 seconds")
        setupHOTSPOT()

def callback_rising(channel):  
    print("raising edge detected on 26") 
    global rt
    if rt !=  None:
        rt.stop();
        rt = None; 
    val =  GPIO.input(26)
    if val == 0:
        print("starting timer")
        rt = RepeatedTimer(5, callback_timer, "reset HOTSPOT")
     
    print(channel)

def callback_falling():
    print("falling edge")

GPIO.add_event_detect(26, GPIO.BOTH, callback=callback_rising, bouncetime=300)
#GPIO.add_event_detect(26, GPIO.RISING, callback=callback_falling, bouncetime=300)

while True:
    time.sleep(0.01)

cancel_event_detect(26)
GPIO.cleanup()
