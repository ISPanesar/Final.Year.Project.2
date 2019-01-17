import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

in1_pin = 4
in2_pin = 17
out1_pin = 20
out2_pin = 21

GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(out1_pin, GPIO.IN)
GPIO.setup(out2_pin, GPIO.IN)

P = GPIO.PWM(in1_pin, 1000)
x = 0
try:
    while 1:
        p.ChangeDutyCycle(x)
        if out1_pin == False:
            if x < 80:
                x = x + 1
                print('faster')
                time.sleep(0.2)
        if out2_pin == False:
            if x > 0:
                x = x -1
                print('slower')
                time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup


