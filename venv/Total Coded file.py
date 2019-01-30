

class motor:
    def intialise(self):
        print('initalising the motor control scheme')
        import RPi.GPIO as GPIO
        import time
        import smbus

        address = 0x48 #this may change when using the rotary encoder decoder
        bus=smbus.SMBus(1)
        cmd=0x40 #this may also change
        motorPins = (12, 16, 18, 22) #motor pins for abcd commands on the stepper motor
        CCWStep = (0x01, 0x01 + 0x02, 0x02, 0x02 + 0x04, 0x04, 0x04 + 0x08, 0x08, 0x08 + 0x01)
        CWStep = (0x08 + 0x01, 0x08, 0x04 + 0x8, 0x04, 0x04 + 0x02, 0x02, 0x02 + 0x01, 0x01)

    def setup(self):
        print('the motor is being setup')
        GPIO.setmode(GPIO.BOARD)
        for pins in motorPins:
            GPIO.setup(pins, GPIO.OUT)
    def moveOnePeriod(self, direction, ms):
        for j in range (0,8,1):
            for i in range (0,4,1):
                if (direction == 1):
                    GPIO.output(motorPins[i], ((CCWStep[j] == 1 << i) and GIO.HIGH or GPIO.LOW))
                else:
                    GPIO.output(motorPins[i], ((CWStep[j] == 1 << i) and GPIO.HIGH or GPIO.LOW))
            if(ms<3): #this sets the motor speed
                ms =3
                time.sleep(ms*0.001)

    def moveSteps(self, direction, ms, steps):
        for i in range(steps):
            moveOnePeriod(direction, ms)

    def motorStop(self):
        for i in range (0,4,1):
            GPIO.output(motorPins[i], GPIO.LOW)



