import smbus2
import time
import threading
import logging


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
        self.relay_state = 0x00
        self.relay_number_active = None
        self.pump_operation_mode = "auto" # oder "manuell", Default = "auto"


    def set_relay_state(self, relay_number, state):
        # relay_number: 1-4
        # state: 1 (ON) or 0 (OFF)
        if state: # switch on
            self.relay_state |= 1 << (relay_number - 1)

        else: # switch off
            self.relay_state &= ~(1 << (relay_number - 1))


        try:
            # set relay state 
            self.bus.write_byte_data(self.address, 0x10, self.relay_state)
            print(f"Setting Relay {relay_number} to state {state} at address {self.address}")
        except Exception as e:
            print(f"Fehler beim Setzen des Relaiszustands: {e}")

    def run(self):
        """Overwrite Thread.run(), called when the thread is started"""
        
        # Prepariert den Pumpprozess
        self._getPumpRelayNumber()
        self._preparePumpOperation()
        logging.info(f"Pump prozess prepared with mode {self.pump_operation_mode} and pump {self.relay_number_active}")

        # Startet den Pumpprozess
        self._runPump()

        # Workaround: Wegen dem Manuell-Mode zur Entlüftung, unterscheiden wir zwischen auto und manuell.
        # Manuell gilt die while-Schlaufe, auto die sleep funktion.
        # TODO: Umbauen!

        if self.pump_operation_mode == "auto":
            time.sleep(self.pump_duration_calculated)
        
        elif self.pump_operation_mode == "manuell":
            while self.event.is_set() == False:
                #self.mix_drink()
                time.sleep(0.1)
        
        # Stops the pump
        self._stopPump()


    def setEvent(self):
        # Is used to stop the pump
        self.event.set()


    def _preparePumpOperation(self):
        # Prepariert die Pump-Prozess
        
        # calculate pump duration
        self.pump_duration()


    def _getPumpRelayNumber(self):
        # Helper function use the right bottle/pump
        
        if self.ingredient_name == "Cola":
            self.relay_number_active = 1
            self.pump_operation_mode = "auto"

        elif self.ingredient_name == "Limettensaft":
            self.relay_number_active = 2
            self.pump_operation_mode = "auto"
        
        elif self.ingredient_name == "Orangensaft":
            self.relay_number_active = 3
            self.pump_operation_mode = "auto"
        
        elif self.ingredient_name == "Sodawasser":
            self.relay_number_active = 4
            self.pump_operation_mode = "auto"
        
        # Diese sind für die Entlüftung da.
        elif self.ingredient_name == "Pumpe 1":    
            self.relay_number_active = 1
            self.pump_operation_mode = "manuell"

        elif self.ingredient_name == "Pumpe 2":
            self.relay_number_active = 2
            self.pump_operation_mode = "manuell"

        elif self.ingredient_name == "Pumpe 3":
            self.relay_number_active = 3
            self.pump_operation_mode = "manuell"
        
        elif self.ingredient_name == "Pumpe 4":
            self.relay_number_active = 4
            self.pump_operation_mode = "manuell"
        

    
    def _runPump(self):
        # switches on pump
        
        self.set_relay_state(relay_number=self.relay_number_active, state=1)
        logging.info(f"Running pump {self.relay_number_active}")
        


    def _stopPump(self):
        # switches off pump
        
        self.set_relay_state(relay_number=self.relay_number_active, state=0)
        logging.info(f"Stopping pump {self.relay_number_active}")

        # Stops the loop
        self.event.set()


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

        elif self.ingredient_name == "Orangensaft":
            # calculate pump duration
            self.pump_duration()
            # switch on Relais 3
            self.set_relay_state(relay_number=3, state=1)
            print("mixing orangensaft")
            time.sleep(self.pump_duration_calculated)
            # switch off Relais 3
            self.set_relay_state(relay_number=3, state=0)
            print("orangensaft mixed")

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

        # Stops the loop
        self.event.set()

            
    def pump_duration(self):
        # calculate amount of ingredient in ml
        amount_ingredient_ml = self.amount_ingredient * 10

        # calculate pump duration in minutes
        pump_time_min = amount_ingredient_ml / self.flow_rate_ml_per_min

        # print calculated pump duration
        logging.info(f"Pumping {self.amount_ingredient} cl (equivalent to {amount_ingredient_ml} ml)")
        logging.info(f"Pump time: {pump_time_min:.2f} minutes")

        # calculate pump duration in seconds
        self.pump_duration_calculated = pump_time_min * 60