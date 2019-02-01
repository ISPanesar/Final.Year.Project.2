#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

def setup():
    GPIO.setmode(GPIO.BCM) # Set GPIO as PIN Numbers
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pull up to high level(3.3V)


def detect():
    print('The count is d%, the step time is %d ') % (count, rotationtime)
    if GPIO.input(17) == False:
        currenttime = time.time()
        print('Clear')
        while GPIO.input(17) == False:
            time.sleep(0.01)
        count = count + 1
        rotationtime = time.time() - currenttime
    else:
        print('Obstructed')


def loop():
    while True:
        detect()

def destroy():
    GPIO.cleanup() # Release resource


if __name__ == '__main__': # Set the Program start from here
    setup()
    try:
        global count
        count = 0
        loop()
    except KeyboardInterrupt: # When pressed 'Ctrl+C' child program destroy() will be executed.
        destroy()

