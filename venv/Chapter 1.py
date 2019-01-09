import RPi.GPIO as GPIO
import time

ledpin = 17

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledpin, GPIO.OUT, initial=0)
    print('using pin%d'%ledpin)

def loop():
    while True:
        GPIO.output(ledpin, GPIO.HIGH)
        print ('...led on')
        time.sleep(1)
        GPIO.output(ledpin, GPIO.LOW)
        print ('led off...')
        time.sleep(1)

def destroy():
    GPIO.output(ledpin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:

        destroy()