
import RPi.GPIO as GPIO
from WeightSensor.hx711 import HX711
import time, sys
import threading
import logging

class WeightSensor(threading.Thread):
    """Threaded Weight Sensor Class"""
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.hx = HX711(5, 6)
        self.initHX()
        self.event = None

    def initHX(self):
        """Initialize the scale"""
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(92000)
        self.hx.reset()
        self.hx.tare()
        print("Tare done! Add weight now...")

    def run(self):
        """Overwrite Thread.run(), called when the thread is started"""
        while True:
            self.read_weight()
            time.sleep(0.5)

    def setEvent(self, event):
        """Set the event object to use for stopping this thread"""
        self.event = event

    def tare(self):
        """Tare the scale"""
        self.hx.tare()
        logging.info("weighing scale tared")


    def reset(self):
        """Reset the scale"""
        self.hx.reset()
        logging.info("weighing scale resetted")

    def cleanAndExit(self):
        """Clean up GPIO pins"""
        print("Cleaning...")
        GPIO.cleanup()       
        print("Bye!")
        sys.exit()

    def read_weight(self):
        """Read the weight from the scale"""
        try:
            val = self.hx.get_weight(5)
            val_calculated = val * 100
            val_rounded = int(round(val_calculated, 2))
            val_units = "{:d} grams".format(val_rounded)
            print(val_units)
            #logging.info("weight: {0}: ".format(val_units))

            self.hx.power_down()
            self.hx.power_up()
            time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            self.cleanAndExit()


# ws = WeightSensor()
# ws.read_weight()



