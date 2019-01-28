
import RPi.GPIO as GPIO
import time




    
def destroy():
    GPIO.input(ledpin, GPIO.LOW)
    GPIO.cleanup()

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)
    global ledpin 
    ledpin = GPIO.input(17)
    print('using pin%d'%ledpin)
    try:
        while True:
            if (ledpin is GPIO.HIGH):
                print ('...led on')
                time.sleep(1)
            elif (ledpin is GPIO.LOW):
                print ('led off...')
                time.sleep(1)
            else:
                print('fuck you')
    except KeyboardInterrupt:

        destroy()
