import RPi.GPIO as GPIO
import smbus
import time


address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40
Z_Pin = 12


def analogRead(chn):
    bus.write_byte(address, cmd+chn)
    value = bus.read_byte(address)
    value = bus.read_byte(address)
    #value = bus.read_byte_data(address, cmd+chn)
    return value


def analogWrite(value):
    bus.write_byte_data(address, cmd, value)


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Z_Pin, GPIO.IN, GPIO.PUD_UP)


def loop():
    while True:
        val_Z = GPIO.input(Z_Pin)
        val_Y = analogRead(0)
        val_X = analogRead(1)
        print('value_X: %d , \tvlue_Y: %d ,\tvlue_z: %d' %(val_X, val_Y, val_Z))
        time.sleep(0.01)


def destroy():
    bus.close()
    GPIO.cleanup()


if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
