import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)
GPIO.setup(20, GPIO.IN)
GPIO.setup(16, GPIO.OUT)
p = GPIO.PWM(16, 100)
p.start(0)


def loop():
    x = 0
    while True:
        p.ChangeDutyCycle(x)
        if (GPIO.input(21) == False):
            if (x < 50):
                print('POWERRRRR')
                x = x + 1
                time.sleep(0.2)
            if (GPIO.input(20) == False):
                if (x > 0):
                    print('SLOWWWWW')
                    x = x - 1
                    time.sleep(0.2)


if __name__ == '__main__':
    print('Program is starting')
    try:
        loop()

    except KeyboardInterrupt:
        GPIO.cleanup

