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

logging.info("Starting the Cocktail Mixer")


class Main:
    def __init__(self):
        self.orderqueue = drinkprocessor.OrderQueue()
        self.recipe = None
        self.stepm = None
        self.servm = None
        self.relayb = None
        self.weights = None
    

    

    def CallOrderQueue(self):
        logging.info("Calling CallOrderQueue")
        
        print("Number of orders in queue: {0}".format(len(self.orderqueue.getOrderQueue()))) 

        # print the order queue
        for order in self.orderqueue.getOrderQueue():
            print("*"*20)
            print("Order: {0}, Name: {1}".format(order.getRecipe(), order.getRecipe().name)) 
            print("*"*20)
              
        # process the order queue
        self.orderqueue.processOrderQueue()


    def CallReferenceRun(self):
        logging.info("Calling ReferenceRun")
        self.stepm = StepperMotor(0)
        self.stepm.reference_run()
        print(globals.current_position)

        


if __name__ == "__main__":
    # Create an instance of the Main class

    if True:
        visu = MyCocktailmixerApp()
        visu.run()

        #main = Main()
        
        #main.CallReferenceRun()
    else:

        rlboard = RelayBoard(None, None)
        rlboard.set_relay_state(1, 0)
        rlboard.set_relay_state(2, 0)
        rlboard.set_relay_state(3, 0)
        rlboard.set_relay_state(4, 0)

    

        """
        main = Main()
        main.CallReferenceRun()
        drinkprocessor = drinkprocessor.OrderQueue()
        recipe = drinkprocessor.Recipe(search_string="")
        drinkprocessor.addOrder(recipe)
        """

    # Call the WeightSensor and run in a thread
    #main.CallWeightSensor()


    # Call the CallDrinkProcessor method
    #main.IncomingDrinkOrder("Bacardi")
    #main.IncomingDrinkOrder("Tuxedo")

    
    
    # Call the CallStepperMotor method
    #main.CallStepperMotor()

    # Call the CallServoMotor method
    #main.CallServoMotor()

    # Call the CallRelayBoard method
    #main.CallRelayBoard()
    
    
    
