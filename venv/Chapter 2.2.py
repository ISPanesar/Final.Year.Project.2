import RPi.GPIO as GPIO

ledPin = 17
buttonPin = 18
ledState = False


def setup():
    print('Program is starting...')
    GPIO.setmode(GPIO.BCM)              #This is the printed circuit numbers
    GPIO.setup(ledPin, GPIO.OUT)        #Set ledPin mode as an output
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)      #Set buttonPin mode as an input


def buttonEvent(channel):
    global ledState
    print ('buttonEvent GPIO%d' %channel)
    ledState = not ledState
    if ledState:
        print ('Turn on LED...')
    else:
        print ('Turn off LED...')
    GPIO.output(ledPin, ledState)


def loop():
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=buttonEvent, bouncetime=300)
    while True:
        pass


def destroy():
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__' :
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()


