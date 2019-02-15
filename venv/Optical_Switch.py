#!/usr/bin/env python
import RPi.GPIO as GPIO
import time


def setup():
    GPIO.setmode(GPIO.BCM) # Set GPIO as PIN Numbers
    GPIO.setup(5, GPIO.IN) # Set pull up to high level(3.3V)
    GPIO.setup(6, GPIO.IN)
    GPIO.add_event_detect(5, GPIO.RISING, bouncetime = 200)
    GPIO.add_event_detect(6, GPIO.RISING, bouncetime = 200)



def loop():
    global count
    count = 0
    global rotationtime
    currenttime = time.time()
    while True:
        """and (GPIO.input(5) == False)) or\((GPIO.input(6) == False) and (GPIO.input(5) == True))"""
        if GPIO.event_detected(5) and GPIO.event_detected(6):


            count = count + 1
            rotationtime = time.time() - currenttime
            print('The count is %s' % count)
        elif time.time() - currenttime > 60:
            RPM = count/(time.time()-currenttime)*60/2
            print(str(RPM))
            currenttime = time.time()
            count = 0
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

