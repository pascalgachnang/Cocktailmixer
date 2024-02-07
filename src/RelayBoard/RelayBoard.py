import smbus2
import time

class RelayBoard:
    def __init__(self, i2c_bus, address):
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = address

    def set_relay_state(self, relay_number, state):
        # relay_number: 1-4
        # state: 1 (ON) or 0 (OFF)
        try:
            # set relay state 
            self.bus.write_byte_data(self.address, relay_number, state)
        except Exception as e:
            print(f"Fehler beim Setzen des Relaiszustands: {e}")

    def mix_drink(self, drink_type):
        try:
            if drink_type == "Cola":
                # switch on relais 1 for 2 seconds
                self.set_relay_state(relay_number=1, state=1)
                print("mixing cola")
                time.sleep(2)
                # switch off relais 1
                self.set_relay_state(relay_number=1, state=0)
                print("cola mixed")

            elif drink_type == "Limettensaft":
                # switch on Relais 2 for 2 seconds
                self.set_relay_state(relay_number=2, state=1)
                print("mixing lemonade")
                time.sleep(2)
                # switch off Relais 2
                self.set_relay_state(relay_number=2, state=0)
                print("lemonade mixed")

            elif drink_type == "Tonic Water":
                # switch on Relais 3 for 2 seconds
                self.set_relay_state(relay_number=3, state=1)
                print("mixing tonic water")
                time.sleep(2)
                # switch off Relais 3
                self.set_relay_state(relay_number=3, state=0)
                print("tonic water mixed")

            elif drink_type == "Sodawasser":
                # switch on Relais 4 for 2 seconds
                self.set_relay_state(relay_number=4, state=1)
                print("mixing soda")
                time.sleep(2)
                # switch off Relais 4
                self.set_relay_state(relay_number=4, state=0)
                print("soda mixed")

            else:
                print("Invalid drink type.")

        except KeyboardInterrupt:
            pass
        


