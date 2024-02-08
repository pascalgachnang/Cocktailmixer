import smbus2
import time
import threading

class RelayBoard(threading.Thread):
    def __init__(self, amount_ingredient, ingredient_name, i2c_bus=1, address=0x11):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = address
        self.amount_ingredient = amount_ingredient
        self.ingredient_name = ingredient_name
        self.pump_duration_calculated = None
        self.flow_rate_ml_per_min = 700  # Durchflussrate der Pumpe in ml/min

    def set_relay_state(self, relay_number, state):
        # relay_number: 1-4
        # state: 1 (ON) or 0 (OFF)
        try:
            # set relay state 
            self.bus.write_byte_data(self.address, relay_number, state)
        except Exception as e:
            print(f"Fehler beim Setzen des Relaiszustands: {e}")

    def run(self):
        """Overwrite Thread.run(), called when the thread is started"""
        while self.event.is_set() == False:
            self.mix_drink()
            time.sleep(0.5)

    def mix_drink(self):
        if self.ingredient_name == "Cola":
            # calculate pump duration
            self.pump_duration()
            # switch on relais 1
            self.set_relay_state(relay_number=1, state=1)
            print("mixing cola")
            time.sleep(self.pump_duration_calculated)
            # switch off relais 1
            self.set_relay_state(relay_number=1, state=0)
            print("cola mixed")

        elif self.ingredient_name == "Limettensaft":
            # calculate pump duration
            self.pump_duration()
            # switch on Relais 2 
            self.set_relay_state(relay_number=2, state=1)
            print("mixing lemonade")
            time.sleep(self.pump_duration_calculated)
            # switch off Relais 2
            self.set_relay_state(relay_number=2, state=0)
            print("lemonade mixed")

        elif self.ingredient_name == "Tonic Water":
            # calculate pump duration
            self.pump_duration()
            # switch on Relais 3
            self.set_relay_state(relay_number=3, state=1)
            print("mixing tonic water")
            time.sleep(self.pump_duration_calculated)
            # switch off Relais 3
            self.set_relay_state(relay_number=3, state=0)
            print("tonic water mixed")

        elif self.ingredient_name == "Sodawasser":
            # calculate pump duration
            self.pump_duration()
            # switch on Relais 4
            self.set_relay_state(relay_number=4, state=1)
            print("mixing soda")
            time.sleep(self.pump_duration_calculated)
            # switch off Relais 4
            self.set_relay_state(relay_number=4, state=0)
            print("soda mixed")

        self.event.set()

            
    def pump_duration(self):
        # calculate amount of ingredient in ml
        amount_ingredient_ml = self.amount_ingredient * 10

        # calculate pump duration in minutes
        pump_time_min = amount_ingredient_ml / self.flow_rate_ml_per_min

        # print calculated pump duration
        print(f"Pumping {self.amount_ingredient} cl (equivalent to {amount_ingredient_ml} ml)")
        print(f"Pump time: {pump_time_min:.2f} minutes")

        # calculate pump duration in seconds
        self.pump_duration_calculated = pump_time_min * 60