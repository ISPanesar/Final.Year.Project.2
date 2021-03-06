# code to run the syringe pump.
# import the current time and the GPIO module.
import time
import RPi.GPIO as GPIO
# Import the ADS1x15 module.
import ADS1x15
# This imports the pigpio module and the HX711 module for the load cell
import pigpio  # http://abyz.co.uk/rpi/pigpio/python.html
import HX711
import threading
import queue
import array as arr





# This is the class for the HX711 sensor module

class sensor:
    # This sets the value assigned to each gain
    CH_A_GAIN_64 = 0
    CH_A_GAIN_128 = 1
    CH_B_GAIN_32 = 2

    # This sets the clocking rate
    DATA_CLKS = 24
    X_128_CLK = 25
    X_32_CLK = 26
    X_64_CLK = 27

    # This sets the pulse length and the timeout limit
    PULSE_LEN = 15
    TIMEOUT = ((X_64_CLK + 3) * 2 * PULSE_LEN)
    SETTLE_READINGS = 5

    """
    A class to read the HX711 24-bit ADC.
    """

    def __init__(self, pi, DATA, CLOCK, mode=CH_A_GAIN_128, callback=None):
        """
        Instantiate with the Pi, the data GPIO, and the clock GPIO.

        Optionally the channel and gain may be specified with the
        mode parameter as follows.

        CH_A_GAIN_64  - Channel A gain 64
        CH_A_GAIN_128 - Channel A gain 128
        CH_B_GAIN_32  - Channel B gain 32

        Optionally a callback to be called for each new reading may be
        specified.  The callback receives three parameters, the count,
        the mode, and the reading.  The count is incremented for each
        new reading.
        """
        self.pi = pi
        self.DATA = DATA
        self.CLOCK = CLOCK
        self.callback = callback

        self._paused = True
        self._data_level = 0
        self._clocks = 0

        self._mode = CH_A_GAIN_128
        self._value = 0

        self._rmode = CH_A_GAIN_128
        self._rval = 0
        self._count = 0

        self._sent = 0
        self._data_tick = pi.get_current_tick()
        self._previous_edge_long = False
        self._in_wave = False

        self._skip_readings = SETTLE_READINGS

        pi.write(CLOCK, 1)  # Reset the sensor.

        pi.set_mode(DATA, pigpio.INPUT)

        pi.wave_add_generic(
            [pigpio.pulse(1 << CLOCK, 0, PULSE_LEN),
             pigpio.pulse(0, 1 << CLOCK, PULSE_LEN)])

        self._wid = pi.wave_create()

        self._cb1 = pi.callback(DATA, pigpio.EITHER_EDGE, self._callback)
        self._cb2 = pi.callback(CLOCK, pigpio.FALLING_EDGE, self._callback)

        self.set_mode(mode)

    def get_reading(self):
        """
        Returns the current count, mode, and reading.

        The count is incremented for each new reading.
        """
        return self._count, self._rmode, self._rval

    def set_callback(self, callback):
        """
        Sets the callback to be called for every new reading.
        The callback receives three parameters, the count,
        the mode, and the reading.  The count is incremented
        for each new reading.

        The callback can be cancelled by passing None.
        """
        self.callback = callback

    def set_mode(self, mode):
        """
        Sets the mode.

        CH_A_GAIN_64  - Channel A gain 64
        CH_A_GAIN_128 - Channel A gain 128
        CH_B_GAIN_32  - Channel B gain 32
        """
        self._mode = mode

        if mode == CH_A_GAIN_128:
            self._pulses = X_128_CLK
        elif mode == CH_B_GAIN_32:
            self._pulses = X_32_CLK
        elif mode == CH_A_GAIN_64:
            self._pulses = X_64_CLK
        else:
            raise ValueError

        self.pause()
        self.start()

    def pause(self):
        """
        Pauses readings.
        """
        self._skip_readings = SETTLE_READINGS
        self._paused = True
        self.pi.write(self.CLOCK, 1)
        time.sleep(0.002)
        self._clocks = DATA_CLKS + 1

    def start(self):
        """
        Starts readings.
        """
        self._wave_sent = False
        self.pi.write(self.CLOCK, 0)
        self._clocks = DATA_CLKS + 1
        self._value = 0
        self._paused = False
        self._skip_readings = SETTLE_READINGS

    def cancel(self):
        """
        Cancels the sensor and release resources.
        """
        self.pause()

        if self._cb1 is not None:
            self._cb1.cancel()
            self._cb1 = None

        if self._cb2 is not None:
            self._cb2.cancel()
            self._cb2 = None

        if self._wid is not None:
            self.pi.wave_delete(self._wid)
            self._wid = None

    def _callback(self, gpio, level, tick):

        if gpio == self.CLOCK:

            if level == 0:

                self._clocks += 1

                if self._clocks <= DATA_CLKS:

                    self._value = (self._value << 1) + self._data_level

                    if self._clocks == DATA_CLKS:

                        self._in_wave = False

                        if self._value & 0x800000:  # unsigned to signed
                            self._value |= ~0xffffff

                        if not self._paused:

                            if self._skip_readings <= 0:

                                self._count = self._sent
                                self._rmode = self._mode
                                self._rval = self._value

                                if self.callback is not None:
                                    self.callback(self._count, self._rmode, self._rval)

                            else:
                                self._skip_readings -= 1

        else:

            self._data_level = level

            if not self._paused:

                if self._data_tick is not None:
                    current_edge_long = pigpio.tickDiff(
                        self._data_tick, tick) > TIMEOUT

                if current_edge_long and not self._previous_edge_long:

                    if not self._in_wave:
                        self._in_wave = True

                        self.pi.wave_chain(
                            [255, 0, self._wid, 255, 1, self._pulses, 0])

                        self._clocks = 0
                        self._value = 0
                        self._sent += 1

            self._data_tick = tick
            self._previous_edge_long = current_edge_long


def motorsetup():
    # This is used to set the GPIO's needed for the L293D motor driver and start PWM
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    global motoRPin1, motoRPin2, enablePin
    motoRPin1 = 27
    motoRPin2 = 17
    enablePin = 22
    GPIO.setup(motoRPin1, GPIO.OUT)
    GPIO.setup(motoRPin2, GPIO.OUT)
    GPIO.setup(enablePin, GPIO.OUT)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(6, GPIO.FALLING)
    GPIO.setmode(GPIO.BCM)  # Set GPIO as PIN Numbers
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pull up to high level(3.3V)
    GPIO.add_event_detect(5, GPIO.FALLING)
    print('motor setting up... ')



def adcsetup():
    # Create an ADS1015 ADC (12-bit) instance.
    global adc
    adc = ADS1x15.ADS1015()

    # Note you can change the I2C address from its default (0x48), and/or the I2C
    # bus by passing in these optional parameters:
    # adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

    # Choose a gain of 1 for reading voltages from 0 to 4.09V.
    # Or pick a different gain to change the range of voltages that are read:
    #  - 2/3 = +/-6.144V
    #  -   1 = +/-4.096V
    #  -   2 = +/-2.048V
    #  -   4 = +/-1.024V
    #  -   8 = +/-0.512V
    #  -  16 = +/-0.256V
    # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
    global GAIN
    GAIN = 1
    print('adc setting up...')


def initialise(c):
    '''GPIO.output(motoRPin1, GPIO.HIGH)
    GPIO.output(motoRPin2, GPIO.LOW)
    p = GPIO.PWM(enablePin, 1000)
    p.start(100)'''
    print('Reading ADS1x15 values, press Ctrl-C to quit...')
    # Print nice channel column headers.
    print('-' * 37)
    # Main loop.
    # This is used to pull data from the load cell

    # This sets the column headings
    print("| Step | Position | Force | RPM | Mode | Raw HX711 | Raw Pot |")
    global counts, RPM, count, values, starttime, forceSP, trackrate, operational_mode, syringelength, rate
    counts = 0
    count = 0
    values = 1499
    rotationtime = 0
    starttime = time.time()
    RPM = 0
    operational_mode = int(input('Do you want constant force(1) or constant flowrate(2)? '))
    if operational_mode == 1:
        print('Constant force selected')
        forceSP = int(input('please enter the required force in Newtons between XX and XX '))
        print('the force the controller will attempt to output is ' + str(forceSP) + 'N')
        syringelength = int(((int(values) - 92) / (1499 - 92)) * 110)
        print(str(syringelength) + 'mm')
    elif operational_mode == 2:
        print('Constant flowrate selected')
        print('This flowrate is defined via the volume expelled vs distance along the track')
        selc = int(input('Do you want to calculate volume with syringe data(1) or just input the volumetric flowrate needed?(2) '))
        values = adc.read_adc(0, gain=GAIN)
        values2 = adc.read_adc(1, gain=GAIN)
        syringelength = int(((int(values) - 92) / (1499 - 92)) * 110)
        diameter = int((-0.0198 * values2 + 40.606))
        area = 3.14195 * (diameter / 2) ** 2
        if selc == 1:
            vol = area * syringelength
            print(str(area) + ' square mm, ' + str(vol) + ' cubic mm')
            tm = int(input('How long do you want the syringe to empty for?'))
            rate = vol/tm
            print('the volumetric flowrate is ' + str(rate))
            trackrate = rate/area
        elif selc == 2:
            volumetricflowrate = int(input('Please enter the volumetric flowrate desired in cubic mm? '))
            trackrate = volumetricflowrate/area
        print('the defined trackrate the controller will try to maintain is ' + str(trackrate) + ' mm/s')
    return c


class motor_control:
    def rpm_measurements(self,  starttime):
        if GPIO.event_detected(5):
            global counts, RPM
            counts = counts + 1
        if (time.time() - starttime) >= 0.01:
            RPM = counts / (2*(time.time() - starttime))
            starttime = time.time()
            counts = 0
        return RPM, starttime

    def motor_start(self, pwm, freq, direction):
        self.p = GPIO.PWM(enablePin, freq)
        self.p.start(pwm)
        if direction == 1:
            GPIO.output(motoRPin1, GPIO.HIGH)
            GPIO.output(motoRPin2, GPIO.LOW)
            print('motor starting, moving forwards')
        elif direction == 0:
            GPIO.output(motoRPin2, GPIO.HIGH)
            GPIO.output(motoRPin1, GPIO.LOW)
            print('motor starting, moving backwards')
        else:
            print('motor has not been correctly started, you need the PWM on time 0-100, clockrate in Hz and directionality 1 is forwards and 0 is backwards')
mc = motor_control()

def loop():
    pi = pigpio.pi()
    if not pi.connected:
        exit(0)
    s = HX711.sensor(pi, DATA=20, CLOCK=21, mode=HX711.CH_B_GAIN_32)
    s.set_mode(HX711.CH_A_GAIN_64)
    c, mode, reading = s.get_reading()
    mc.motor_start(100, 1000, 1)
    RPM = 0
    while True:
        #que = queue.Queue()
        que2 = queue.Queue()
        # Read the ADC channel values in a list.
        #t = threading.Thread(target=lambda q, arg1: q.put(adc.read_adc(0, gain=GAIN)), args=(que, 1))
        #t.start()
        #t.join()
        #nonlocal values
        values = adc.read_adc(0, gain=GAIN)
        count, mode, reading = s.get_reading()
        #while not que.empty():
        #    values = que.get()
        #    count, mode, reading = s.get_reading()


        """ This calculates the force on the load cell, the distance
        along the track the syringe has moved and outputs the raw data along 
        with the number of steps"""
        mcr = threading.Thread(target=lambda q, arg1: q.put(mc.rpm_measurements(starttime)), args=(que2, 1))
        mcr.start()
        mcr.join()
        while not que2.empty():
            RPM = que2.get()


        if count != c:
            c = count
            Force = 0.00004 * (reading - 283000)
            length = 110 - (((int(values) - 92) / (1499 - 92)) * 110)
            print("| {} | {} | {} | {} | {} | {} | {} |".format(count, str(round(length, 2)) + "mm",
                                                                     str(round(Force, 5)) + "N",
                                                                     str(round(RPM, 0)), mode, reading, values))

        """90 is the limit of the track so the system moves to the end of the track 
        before reversing 1500 is the start of the track """
        if values < 140:
            GPIO.output(motoRPin2, GPIO.HIGH)
            GPIO.output(motoRPin1, GPIO.LOW)
            print('Reversing')
        ''' elif values > 2046:
            GPIO.output(motoRPin1, GPIO.LOW)
            GPIO.output(motoRPin2, GPIO.LOW)
            print('stopping')
            GPIO.cleanup()
            exit()
            """Please note that the Force and length of the track needs to be 
            calibrated to be used with this program apply a known force to the 
            load cell and use this to calibrate the raw data, use a set of calipers
            to determine the length of the track and use the program to see the
            raw data limitations for the hardware"""
'''

def forceloop():
    pi = pigpio.pi()
    if not pi.connected:
        exit(0)
    s = HX711.sensor(pi, DATA=20, CLOCK=21, mode=HX711.CH_B_GAIN_32)
    s.set_mode(HX711.CH_A_GAIN_64)
    c, mode, reading = s.get_reading()
    pwm = 50
    mc.motor_start(pwm, 1000, 1)
    RPM = 0
    while True:
        # que = queue.Queue()
        que2 = queue.Queue()
        # Read the ADC channel values in a list.
        # t = threading.Thread(target=lambda q, arg1: q.put(adc.read_adc(0, gain=GAIN)), args=(que, 1))
        # t.start()
        # t.join()
        # nonlocal values
        values = adc.read_adc(0, gain=GAIN)
        count, mode, reading = s.get_reading()
        # while not que.empty():
        #    values = que.get()
        #    count, mode, reading = s.get_reading()

        """ This calculates the force on the load cell, the distance
        along the track the syringe has moved and outputs the raw data along 
        with the number of steps"""
        mcr = threading.Thread(target=lambda q, arg1: q.put(mc.rpm_measurements(starttime)), args=(que2, 1))
        mcr.start()
        mcr.join()
        while not que2.empty():
            RPMmeas = que2.get()
            RPM = RPMmeas[0]


        if count != c:
            c = count
            Force = 0.00004 * (reading - 283000)
            length = (((int(values) - 92) / (1499 - 92)) * 110)
            print("| {} | {} | {} | {} | {} | {} | {} | {} |".format(count, str(round(length, 2)) + "mm",
                                                                str(round(Force, 5)) + "N",
                                                                str(round(RPM, 0)), mode, reading, values, time.time()), file=open("results.txt", "a"))
            print("| {} | {} | {} | {} | {} | {} | {} |".format(count, str(round(length, 2)) + "mm",
                                                                str(round(Force, 5)) + "N",
                                                                str(round(RPM, 0)), mode, reading, values))
            if length <= 0:
                GPIO.output(motoRPin1, GPIO.LOW)
                GPIO.output(motoRPin2, GPIO.LOW)
                print('stopping as syringe is empty')
                GPIO.cleanup()
                exit(0)
            if round(Force,0) - round(forceSP, 0) != 0:
                if round(Force,0 ) - round(forceSP, 0) < 0:
                    if pwm == 100:
                        print('the motor cannot turn faster')
                    elif pwm < 100:
                        pwm = pwm + 1
                        mc.p.ChangeDutyCycle(pwm)
                else:
                    if pwm == 0:
                        print('the motor has stalled')
                        pwm = 100
                        mc.p.ChangeDutyCycle(pwm)
                        GPIO.output(motoRPin2, GPIO.HIGH)
                        GPIO.output(motoRPin1, GPIO.LOW)
                        time.sleep(2)
                        GPIO.output(motoRPin1, GPIO.HIGH)
                        GPIO.output(motoRPin2, GPIO.LOW)
                        pwm = 1
                        mc.p.ChangeDutyCycle(pwm)
                        print('restarting motor')
                        time.sleep(1)
                    elif pwm > 0:
                        pwm = pwm -1
                        mc.p.ChangeDutyCycle(pwm)


def trackloop():
    pi = pigpio.pi()
    if not pi.connected:
        exit(0)
    s = HX711.sensor(pi, DATA=20, CLOCK=21, mode=HX711.CH_B_GAIN_32)
    s.set_mode(HX711.CH_A_GAIN_64)
    c, mode, reading = s.get_reading()
    pwm = 50
    mc.motor_start(pwm, 1000, 1)
    RPM = 0
    depressionrate = 0
    global rate
    rate = []
    while True:
        # que = queue.Queue()
        que2 = queue.Queue()
        # Read the ADC channel values in a list.
        # t = threading.Thread(target=lambda q, arg1: q.put(adc.read_adc(0, gain=GAIN)), args=(que, 1))
        # t.start()
        # t.join()
        # nonlocal values
        values = adc.read_adc(0, gain=GAIN)
        count, mode, reading = s.get_reading()
        # while not que.empty():
        #    values = que.get()
        #    count, mode, reading = s.get_reading()

        """ This calculates the force on the load cell, the distance
        along the track the syringe has moved and outputs the raw data along 
        with the number of steps"""
        mcr = threading.Thread(target=lambda q, arg1: q.put(mc.rpm_measurements(starttime)), args=(que2, 1))
        mcr.start()
        mcr.join()
        while not que2.empty():
            RPMmeas = que2.get()
            RPM = RPMmeas[0]

        if count != c:
            c = count
            Force = 0.00004 * (reading - 283000)
            length = (((int(values) - 92) / (1499 - 92)) * 110)
            print("| {} | {} | {} | {} | {} | {} | {} |".format(count, str(round(length, 2)) + "mm",
                                                                str(round(Force, 5)) + "N",
                                                                str(round(RPM, 0)), mode, reading, values), file=open("results1.txt", "a"))
            print("| {} | {} | {} | {} | {} | {} | {} |".format(count, str(round(length, 2)) + "mm",
                                                                str(round(Force, 5)) + "N",
                                                                str(round(RPM, 0)), mode, reading, values))


            tracktime = time.time()
            tracklst = (length, tracktime)
            rate.append(tracklst)
            time.sleep(0.001)
            if length <= 0:
                GPIO.output(motoRPin1, GPIO.LOW)
                GPIO.output(motoRPin2, GPIO.LOW)
                print('stopping as syringe is empty')
                GPIO.cleanup()
                exit(0)
            if len(rate) == 1000:
                dsts, timez = zip(*rate)
                depressionrate = (dsts[0] - dsts[1000]) / (timez[1000] - timez[0])
                rate = rate.pop()
            if round(depressionrate, 0) - trackrate !=0:
                if round(depressionrate, 0) - trackrate < 0:
                    if pwm == 100:
                        print('the motor cannot turn faster')
                    elif pwm < 100:
                        pwm = pwm + 1
                        mc.p.ChangeDutyCycle(pwm)
                    else:
                        if pwm == 0:
                            print('the motor has stalled')
                            pwm = 100
                            mc.p.ChangeDutyCycle(pwm)
                            GPIO.output(motoRPin2, GPIO.HIGH)
                            GPIO.output(motoRPin1, GPIO.LOW)
                            time.sleep(2)
                            GPIO.output(motoRPin1, GPIO.HIGH)
                            GPIO.output(motoRPin2, GPIO.LOW)
                            pwm = 1
                            mc.p.ChangeDutyCycle(pwm)
                            print('restarting motor')
                            time.sleep(1)
                        elif pwm > 0:
                            pwm = pwm - 1
                            mc.p.ChangeDutyCycle(pwm)





if __name__ == '__main__':
    motorsetup()
    adcsetup()
    initialise(0)
    #try:
    #    loop()
    #except KeyboardInterrupt:
    #    GPIO.cleanup()
    if operational_mode == 1:
        try:
            forceloop()
        except KeyboardInterrupt:
            GPIO.cleanup()
    else:
        try:
            trackloop()
        except KeyboardInterrupt:
            GPIO.cleanup()



