import RPi.GPIO as GPIO
import time
import random

pins = {'pin_R':11, 'pin_G':12, 'pin_B':13}

def setup():
    global p_R, p_G, p_B
    print('Program is running...')
    GPIO.setmode(GPIO.BOARD)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.HIGH)
    p_R = GPIO.PWN(pins['pin_R'], 2000)
    p_G = GPIO.PWN(pins['pin_G'], 2000)
    p_B = GPIO.PWN(pins['pin_B'], 2000)
    p_R.start(0)
    p_G.start(0)
    p_B.start(0)


def setColour(r_val, g_val, b_val):
    p_R.ChangeDutyCycle(r_val)
    p_G.ChangeDutyCycle(g_val)
    p_B.ChangeDutyCycle(b_val)

def loop():
    while True:
        r = random.randint(0,100)
        g = random.randint(0,100)
        b = random.randint(0,100)
        setColour(r,g,b)
        print('r=%d, g=%d, b=%d' %(r, g, b))
        time.sleep(0.3)


def destroy():
    p_R.stop()
    p_G.stop()
    p_B.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
