#!/usr/bin/env python
import RPi.GPIO as GPIO
import time






def destroy():
    GPIO.cleanup() # Release resource


if __name__ == '__main__': # Set the Program start from here
    GPIO.setmode(GPIO.BCM) # Set GPIO as PIN Numbers
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pull up to high level(3.3V)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(5, GPIO.FALLING, bouncetime=20)
    try:
        global count
        count = 0
        global rotationtime
        currenttime = time.time()
        while True:
            """and (GPIO.input(5) == False)) or\((GPIO.input(6) == False) and (GPIO.input(5) == True))"""
            if GPIO.event_detected(5):
                # and GPIO.input(6) == True:
                print('event detected')
                #time.sleep(0.05)
                GPIO.wait_for_edge(6, GPIO.FALLING)
                print('event 2 detected')
            # if GPIO.input(5) == False:
            #   print('False')
            else:
                print('Python hates me')
                '''count = count + 1
                rotationtime = time.time() - currenttime
                print('The count is %s' % count)
                time.sleep(0.01)
            elif time.time() - currenttime > 60:
                RPM = count/(time.time()-currenttime)*60/2
                print(str(RPM))
                currenttime = time.time()
                count = 0
            else:
                print('Clear')
                time.sleep(0.01)
            # print('The count is %s, the step time is %s ' % (count, rotationtime))
    '''
    except KeyboardInterrupt: # When pressed 'Ctrl+C' child program destroy() will be executed.
        destroy()

