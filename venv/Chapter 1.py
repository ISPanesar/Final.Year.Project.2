import RPi.GPIO as GPIO
import time



def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)
    global ledpin = GPIO.input(17)
    print('using pin%d'%ledpin)

def loop():
    while True:
        if (ledpin is True):
            print ('...led on')
            time.sleep(1)
        else:
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
