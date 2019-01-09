import RPi.GPIO as GPIO
import time

ledpin = 17
buttonpin = 18


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledpin, GPIO.OUT, initial=0)
    GPIO.setup(buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def loop():
    while True:
        if GPIO.input(buttonpin) == GPIO.LOW:
            GPIO.output(ledpin, GPIO.HIGH)
            print ('...led on')
        else:
            GPIO.output(ledpin, GPIO.LOW)
            print ('led off...')


def destroy():
    GPIO.output(ledpin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
