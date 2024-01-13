import time
import sys

EMULATE_HX711 = False
referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711 
else:
    from emulated_hx711 import HX711

class WeightSensor:

    def cleanAndExit():
        print("Cleaning...")

        if not EMULATE_HX711:
            GPIO.cleanup()
            
        print("Bye!")
        sys.exit()


    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(92000)
    hx.reset()
    hx.tare()
    print("Tare done! Add weight now...")


    while True:
        try:
            val = hx.get_weight(5)
            val_calculated = val * 100
            val_rounded = int(round(val_calculated, 2))
            val_units = "{:d} grams".format(val_rounded)
            print(val_units)

            hx.power_down()
            hx.power_up()
            time.sleep(0.1)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


