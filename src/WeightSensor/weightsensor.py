import RPi.GPIO as GPIO
from WeightSensor.hx711 import HX711
import time, sys
import threading
import logging
import config
import os

class WeightSensor(threading.Thread):
    """Threaded Weight Sensor Class"""
    def __init__(self, amount_ingredient):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.hx = HX711(5, 6)
        self.initHX()
        self.config = config.config
        self.tolerance_weight = self.config.getfloat('WeightSensor', 'tolerance_weight')
        self.amount_ingredient = amount_ingredient
        self.weight_ingredient_gramms = None
        self.val_rounded = None
        self.current_time = None
        self.start_time = None

    def initHX(self):
        """Initialize the scale"""
        self.hx.set_reading_format("MSB", "MSB")
        self.hx.set_reference_unit(92000)
        self.hx.reset()
        self.hx.tare()
        print("Tare done! Add weight now...")

    def run(self):
        """Overwrite Thread.run(), called when the thread is started"""
        while self.event.is_set() == False:
            self.read_weight()
            self.check_amount()
            time.sleep(0.5)

    def stop(self):
        """Stop the thread"""
        self.event.set()

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
        print("Bye!")

    def read_weight(self):
        """Read the weight from the scale"""

        val = self.hx.get_weight()
        val_calculated = val * 100
        self.val_rounded = int(round(val_calculated, 2))
        val_units = "{:d} grams".format(self.val_rounded)
        print(val_units)
        logging.info("weight: {0}: ".format(val_units))

        self.hx.power_down()
        self.hx.power_up()
        time.sleep(0.1)

        




    def check_amount(self):
        """Check if the amount of liquid is enough"""
        self.weight_ingredient_grams = self.amount_ingredient * 10
        if self.weight_ingredient_grams - self.tolerance_weight <= self.val_rounded <= self.weight_ingredient_grams + self.tolerance_weight:
            print("Enough liquid")
            
            
        elif self.val_rounded < self.weight_ingredient_grams - self.tolerance_weight:
            print("Not enough liquid")
            
            
        elif self.val_rounded > self.weight_ingredient_grams + self.tolerance_weight:
            print("Too much liquid")
            
            
        self.event.set()



