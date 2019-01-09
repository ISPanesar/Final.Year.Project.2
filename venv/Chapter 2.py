import RPi.GPIO as GPIO
import time

ledPin = 17
buttonPin = 18


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def loop():
    while True:
        if GPIO.input(buttonPin) == GPIO.LOW:
            GPIO.output(ledPin, GPIO.HIGH)
            print ('led on...')
        else:
            GPIO.output(ledPin, GPIO.LOW)
            print ('led off...')


def destroy():
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
