import RPi.GPIO as GPIO
import time

ledpin = 17

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledpin, GPIO.IN)
    print('using pin%d'%ledpin)

def loop():
    while True:
        if GPIO.input(ledpin, GPIO.HIGH):
            print ('...led on')
            time.sleep(1)
        else:
            GPIO.input(ledpin, GPIO.LOW)
            print ('led off...')
            time.sleep(1)

def destroy():
    GPIO.input(ledpin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:

        destroy()
