import logging
import os
import sys
import time
import json
import config
import drinkprocessor
import secrets
import threading

from StepperMotor.StepperMotor import StepperMotor
from ServoMotor.ServoMotor import ServoMotor
from RelayBoard.RelayBoard import RelayBoard
from WeightSensor.weightsensor import WeightSensor
from visualization import MyCocktailmixerApp



# Create the logs folder if it doesn't exist
logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)

# Configure the logger
logging.basicConfig(filename=os.path.join(logs_folder, 'logfile.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Main:
    def __init__(self):
        self.orderqueue = drinkprocessor.OrderQueue()
        self.recipe = None
        self.stepm = None
        self.servm = None
        self.relayb = None
        self.weights = None
    

    def SimulateDrinkOrder(self, search_string):
        logging.info("Simulating DrinkOrder")
        
        # search for a recipe
        self.recipe = drinkprocessor.Recipe(search_string=search_string)
        
        # add an order to the order queue
        self.orderqueue.addOrder(self.recipe)


    def CallOrderQueue(self):
        logging.info("Calling CallOrderQueue")
        
        print("Number of orders in queue: {0}".format(len(self.orderqueue.getOrderQueue()))) 

        # print the order queue
        for order in self.orderqueue.getOrderQueue():
            print("*"*20)
            print("Order: {0}, Name: {1}".format(order.getRecipe(), order.getRecipe().name))
        
            for ingredient in order.getRecipe().ingredients:
                print("Zutat: {0}, Menge: {1}".format(ingredient.get('ingredient'), ingredient.get('amount')))
                main.CallWeightSensor()
            
            print("*"*20)
              
        # process the order queue
        self.orderqueue.processOrderQueue()


    def CallStepperMotor(self):
        logging.info("Calling StepperMotor")
        self.stepm = StepperMotor(800, 800)
        self.stepm.start()
        self.stepm.join()
        logging.info("Calling StepperMotor: {0}".format(self.stepm))
        #self.stepm._nema17_ramp(8000, 800)
        self.stepm.reference_run()

    def CallServoMotor(self):
        logging.info("Calling ServoMotor")
        self.servm = ServoMotor()
        self.servm.move50ml()

    def CallRelayBoard(self):
        logging.info("Calling RelayBoard")
        self.relayb = RelayBoard(i2c_bus=1, address=0x11)
        
        self.relayb.mix_drink("Cola")
        self.relayb.mix_drink("Lemonade")
        self.relayb.mix_drink("Orange Juice")
        self.relayb.mix_drink("Water")

    def CallWeightSensor(self):
        logging.info("Calling WeightSensor")
        self.weights = WeightSensor()
        self.weights.start()
        time.sleep(3)
        self.weights.stop()

        


if __name__ == "__main__":
    # Create an instance of the Main class

    visu = MyCocktailmixerApp()
    visu.run()

    #main = Main()

    # Call the WeightSensor and run in a thread
    #main.CallWeightSensor()

    # Call the CallDrinkProcessor method
    #main.SimulateDrinkOrder("Mojito")
    #main.SimulateDrinkOrder("Bacardi")
    #main.SimulateDrinkOrder("Tuxedo")

    #main.CallOrderQueue()
    
    # Call the CallStepperMotor method
    #main.CallStepperMotor()

    # Call the CallServoMotor method
    #main.CallServoMotor()

    # Call the CallRelayBoard method
    #main.CallRelayBoard()
    
    
    
