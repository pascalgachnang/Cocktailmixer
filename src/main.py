import logging
import os
import json
import config
import drinkprocessor
import secrets

import StepperMotor.StepperMotor as STEPM
import ServoMotor.ServoMotor as SERVM
import RelayBoard.RelayBoard as RELAYB

# Create the logs folder if it doesn't exist
logs_folder = 'logs'
os.makedirs(logs_folder, exist_ok=True)

# Configure the logger
#logging.basicConfig(filename=os.path.join(logs_folder, 'logfile.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class Main:
    def __init__(self):
        self.orderqueue = drinkprocessor.OrderQueue()
    

    def SimulateDrinkOrder(self, search_string):
        logging.info("Simulating DrinkOrder")
        
        # search for a recipe
        recipe = drinkprocessor.Recipe(search_string=search_string)
        
        # add an order to the order queue
        self.orderqueue.addOrder(recipe)


    def CallOrderQueue(self):
        logging.info("Calling CallOrderQueue")
        
        print("Number of orders in queue: {0}".format(len(self.orderqueue.getOrderQueue()))) 

        # print the order queue
        for order in self.orderqueue.getOrderQueue():
            print("*"*20)
            print("Order: {0}, Name: {1}".format(order.getRecipe(), order.getRecipe().name))
        
            for ingredient in order.getRecipe().ingredients:
                print("Zutat: {0}, Menge: {1}".format(ingredient.get('ingredient'), ingredient.get('amount')))
            
            print("*"*20)
              
        # process the order queue
        self.orderqueue.processOrderQueue()
        


    def CallStepperMotor(self):
        logging.info("Calling StepperMotor")
        stepm = STEPM.StepperMotor()
        stepm.nema17_ramp(8000, 400)

    def CallServoMotor(self):
        logging.info("Calling ServoMotor")
        servm = SERVM.ServoMotor()
        
        servm.move25ml()
        #servm.move50ml()

    def CallRelayBoard(self):
        logging.info("Calling RelayBoard")
        relayb = RELAYB.RelayBoard(i2c_bus=1, address=0x11)
        
        relayb.mix_drink("Cola")
        relayb.mix_drink("Lemonade")
        relayb.mix_drink("Orange Juice")
        relayb.mix_drink("Water")
    
        


if __name__ == "__main__":
    # Create an instance of the Main class
    main = Main()

    # Call the CallDrinkProcessor method
    main.SimulateDrinkOrder("Mojito")
    main.SimulateDrinkOrder("Bacardi")
    main.SimulateDrinkOrder("Tuxedo")

    main.CallOrderQueue()

    # Call the CallStepperMotor method
    main.CallStepperMotor()

    # Call the CallServoMotor method
    main.CallServoMotor()

    # Call the CallRelayBoard method
    main.CallRelayBoard()