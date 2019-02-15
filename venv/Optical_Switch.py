#!/usr/bin/env python
import RPi.GPIO as GPIO
import time


def setup():
    GPIO.setmode(GPIO.BCM) # Set GPIO as PIN Numbers
    GPIO.setup(5, GPIO.IN) # Set pull up to high level(3.3V)
    GPIO.setup(6, GPIO.IN)
    GPIO.add_event_detect(5, GPIO.RISING, bouncetime=200)
    GPIO.add_event_detect(6, GPIO.RISING)



def loop():
    global count
    count = 0
    global rotationtime
    rotationtime = 0
    while True:
        """and (GPIO.input(5) == False)) or\((GPIO.input(6) == False) and (GPIO.input(5) == True))"""
        if GPIO.event_detected(5):
            currenttime = time.time()
            print('Pin 5 high | Pin 6 low')
            GPIO.wait_for_edge(6, GPIO.RISING, bouncetime=200)
            print('Pin 5 &6  high')
            GPIO.wait_for_edge(5, GPIO.FALLING, bouncetime=200)
            print('Pin 5 low | Pin 6 high')
            GPIO.wait_for_edge(6, GPIO.FALLING, bouncetime=200)
            print('Both pins low')

            count = count + 1
            rotationtime = time.time() - currenttime
            print('The count is %s, the step time is %s ' % (count, rotationtime))
        else:
            print('Clear')
        # print('The count is %s, the step time is %s ' % (count, rotationtime))

def destroy():
    GPIO.cleanup() # Release resource


if __name__ == '__main__': # Set the Program start from here
    setup()
    try:

        loop()
    except KeyboardInterrupt: # When pressed 'Ctrl+C' child program destroy() will be executed.
        destroy()

