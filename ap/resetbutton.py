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

GPIOButton = 26

GPIO.setup(GPIOButton, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

source = "source.txt"
target = "target.txt"


def setupHOTSPOT():
    print("setup access point")
    os.system ("./restart_access_point.sh")
    #global source
    #global target
    #copyfile(source,target)


rt = None
timePressed  = 0;
cancelReboot = False

def callback_timer(message):
    global cancelReboot;
    cancelReboot = True; # cancel the reboot
    print(message);
    global GPIOButton
    val=  GPIO.input(GPIOButton)
    global rt
    rt.stop()
    rt = None
    if val == 0:
        # Button is still pressed 
        print("user pressed the reset HOTSPOT button for 5 seconds")
        setupHOTSPOT()



def callback_rising(channel):  
    print("Button event detected") 
    global rt
    global GPIOButton
    global timePressed
    global cancelReboot
    if rt !=  None:
        rt.stop();
        rt = None; 
    val =  GPIO.input(GPIOButton)
    if val == 0:
        print("button pressed starting timer")
        rt = RepeatedTimer(5, callback_timer, "reset HOTSPOT")
        timePressed = time.time();
    if val == 1:
        print("Button unpressed")
        if cancelReboot == False:
            timeUnpressed = time.time();
            interval = int(timeUnpressed - timePressed);
            print(interval)
            if interval >= 1:
              print("Reboot");
              os.system('sudo shutdown -r now')
        else:
            print("reboot was canceled");
            cancelReboot = False;
       
    print(channel)

def callback_falling():
    print("falling edge")

GPIO.add_event_detect(26, GPIO.BOTH, callback=callback_rising, bouncetime=25)
#GPIO.add_event_detect(26, GPIO.RISING, callback=callback_falling, bouncetime=300)
print("ready")

while True:
    time.sleep(0.01)

cancel_event_detect(GPIOButton)
GPIO.cleanup()
