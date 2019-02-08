#!/usr/bin/env python
import RPi.GPIO as GPIO
import time


def setup():
    GPIO.setmode(GPIO.BCM) # Set GPIO as PIN Numbers
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pull up to high level(3.3V)


def loop():
    global count
    count = 0
    global rotationtime
    rotationtime = 0
    while True:
        if GPIO.input(6) == True:
            currenttime = time.time()
            print('obstructed')
            while GPIO.input(6) == True:
                time.sleep(0.01)
            count = count + 1
            rotationtime = time.time() - currenttime
        else:
            print('Clear')
        print('The count is %s, the step time is %s ' % (count, rotationtime))

def destroy():
    GPIO.cleanup() # Release resource


if __name__ == '__main__': # Set the Program start from here
    setup()
    try:

        loop()
    except KeyboardInterrupt: # When pressed 'Ctrl+C' child program destroy() will be executed.
        destroy()

