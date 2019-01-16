import RPi.GPIO as GPIO
import time


motorPins = (12, 16, 18, 22)
CCWStep = (0x01, 0x01 + 0x02, 0x02, 0x02 + 0x04, 0x04, 0x04 + 0x08, 0x08, 0x08 + 0x01)
CWStep = (0x08, 0x04, 0x02, 0x01)


def setup():
    print('Program is starting...')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(38, GPIO.IN)
    GPIO.setup(40, GPIO.IN)
    x = 7
    for pin in motorPins:
        GPIO.setup(pin, GPIO.OUT)


def moveOnePeriod(direction, ms):
    for j in range (0, 8, 1):
        for i in range(0, 4, 1):
            if direction == 1:
                GPIO.output(motorPins[i], ((CCWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
            else:
                GPIO.output(motorPins[i], ((CWStep[j] == 1<<i) and GPIO.HIGH or GPIO.LOW))
            if ms < 1:
                ms = 1
            time.sleep(ms*0.001)


def moveSteps(direction, ms, steps):
    for i in range(steps):
        moveOnePeriod(direction, ms)


def motorStop():
    for i in range(0, 4, 1):
        GPIO.output(motorPins[i], GPIO.LOW)


def loop():
    while True:
        if (GPIO.input(40) == False):
            if (x > 1):
                x = x - 1
                print('Speeding up')
        if (GPIO.input(38) == False):
            if (x < 15):
                x = x + 1
                print('Slowing down')

        moveSteps(1, x, 512)
        time.sleep(0.001)


def destroy():
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
