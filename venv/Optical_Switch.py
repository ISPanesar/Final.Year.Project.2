#!/usr/bin/env python
import RPi.GPIO as GPIO

LightInPin = 17


def setup():
    GPIO.setmode(GPIO.BOARD) # Set GPIO as PIN Numbers
    GPIO.setup(LightInPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pull up to high level(3.3V)
    GPIO.add_event_detect(LightInPin, GPIO.BOTH, callback=detect, bouncetime=200)


def detect():
    if GPIO.input(17) == True:
        print('state 1')
    else:
        print('state 2')


def loop():
    while True:
        detect()


def destroy():
    GPIO.cleanup() # Release resource


if __name__ == '__main__': # Set the Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt: # When pressed 'Ctrl+C' child program destroy() will be executed.
        destroy()

