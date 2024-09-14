import logging
import config
import time
import threading
import queue
from StepperMotor.StepperMotor import StepperMotor
from ServoMotor.ServoMotor import ServoMotor
from RelayBoard.RelayBoard import RelayBoard
from WeightSensor.weightsensor import WeightSensor
from databaseOrders import DatabaseOrders

#from LedRing.LedRing import LedRing





class OrderQueue(threading.Thread):

    def __init__(self, app_instance):
        super().__init__()
        self.app_instance = app_instance
        self.order_queue = queue.Queue()
        self.stepm = StepperMotor()
        self.servm = ServoMotor()
        #self.ledring = LedRing()
        self.drink_in_progress = False
        
        
        
    
    def addOrder(self, recipe):
        # pass in a recipe object
        order = Order("TEST", recipe) 
        self.order_queue.put(order)
        #TODO: Command for sync-move and tuple 

    def run(self):
        # This method is called when the thread is started
        while True:
            order = self.order_queue.get()
            self.drink_in_progress = True
            self.processOrder(order)
            self.drink_in_progress = False
            
    
        

    def processOrder(self, order):
        print("Preparing Recipe: {0}".format(order.getRecipe().name))
        time.sleep(0.5)
        # process the order here ...
        print("*"*20)
        for ingredientDetail in order.getRecipe().ingredients_details:
                
            print("Zutat: {0}, Menge: {1}, Unit: {2}, Type: {3}, Position: {4}".format(ingredientDetail.getName(), \
                                                                                        ingredientDetail.getAmount(), \
                                                                                        ingredientDetail.getUnit(), \
                                                                                        ingredientDetail.getType(), \
                                                                                        ingredientDetail.getPosition()))
            
            
            
            
            logging.info("Zutat: {0}, Menge: {1}, Unit: {2}, Type: {3}, Position: {4}".format(ingredientDetail.getName(), \
                                                                                        ingredientDetail.getAmount(), \
                                                                                        ingredientDetail.getUnit(), \
                                                                                        ingredientDetail.getType(), \
                                                                                        ingredientDetail.getPosition()))
                      
            
        

            if ingredientDetail.getType() == "gravity":
                self.CallStepperMotor(ingredientDetail.getPosition())
                time.sleep(1)
                self.CallServoMotor(ingredientDetail.getAmount())
                self.CallWeightSensor(ingredientDetail.getAmount())
            elif ingredientDetail.getType() == "pumped":
                self.CallStepperMotor(ingredientDetail.getPosition())
                time.sleep(1)
                self.CallRelayBoard(ingredientDetail.getAmount(), ingredientDetail.getName())
                self.CallWeightSensor(ingredientDetail.getAmount())
            elif ingredientDetail.getType() == "manual":
                logging.info("Manual ingredient: {0}".format(ingredientDetail.getName()))
                
            time.sleep(1)

        self.stepm.back_to_startposition()
        
        logging.info("Order processed")

        print("*"*20)
        
                
    def CallStepperMotor(self, position_ingredient):
        logging.info("Calling StepperMotor")
        self.stepm.move(position_ingredient)
        logging.info("Calling StepperMotor: {0}".format(self.stepm))

    def CallServoMotor(self, amount_ingredient):
        logging.info("Calling ServoMotor")
        self.servm.amount_controlling(amount_ingredient)
        logging.info("Calling ServoMotor: {0}".format(self.servm))

    def CallRelayBoard(self, amount_ingredient, ingredient_name):
        logging.info("Calling RelayBoard")
        self.relayb = RelayBoard(amount_ingredient, ingredient_name)
        self.relayb.start()
        self.relayb.join()
        logging.info("Calling RelayBoard: {0}".format(self.relayb))
    
    def CallWeightSensor(self, amount_ingredient):
        logging.info("Calling WeightSensor")
        self.weights = WeightSensor(amount_ingredient)
        self.weights.start()
        self.weights.join()
        logging.info("Calling WeightSensor: {0}".format(self.weights))

    def CallLedRing(self, color):
        logging.info("Calling LedRing")
        self.ledring.set_color(color)
        logging.info("Calling LedRing: {0}".format(self.ledring))


class Order():
    
        def __init__(self, name=None, recipe=None):
            self.name = name
            self.recipe = recipe
            self.customer = None

        def setName(self, name):
            self.name = name
    
        def getName(self):
            return self.name
        
        def setCustomer(self, customer):
            self.customer = customer   

        def getCustomer(self):
            return self.customer
        
        def setRecipe(self, recipe):
            self.recipe = recipe

        def getRecipe(self):
            return self.recipe

        

class Customer():

    def __init__(self, name=None):
        self.name = name

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name


class Recipe():
    # This class is used to store the details of a recipe
    def __init__(self, search_string=None):
        
        self.search_string = search_string
        self.recipe = None
        self.name = None
        self.ingredients = []
        self.ingredients_details = []
        self.db = DatabaseOrders()


        self.findRecipes()


    def findRecipes(self):
        # search for a recipe
        logging.info("Reading recipes")
        
        for recipe in config.recipes:

            if recipe.get('name') == self.search_string:

                msg = "Rezept: {0}, Anzahl: {1}".format(recipe.get('name'), len(config.recipes))
                order = self.search_string
                logging.info(msg)
                self.recipe = recipe
                self.name = recipe.get('name')
                self.ingredients = recipe.get('ingredients')

                #Dictionary to store the ingredients
                ingredients_dict = {}

                for ingredient in recipe.get('ingredients'):
                    msg = "Ingredient: {0}, Menge: {1}, Unit: {2}".format(ingredient.get('ingredient'), ingredient.get('amount'), ingredient.get('unit'))
                    logging.info(msg)

                    ingredientDetails = IngredientDetails()
                    ingredientDetails.setName(ingredient.get('ingredient'))
                    ingredientDetails.setAmount(ingredient.get('amount'))
                    ingredientDetails.setUnit(ingredient.get('unit'))

                    #Store the ingredients in a dictionary
                    ingredients_dict[ingredient.get('ingredient')] = ingredient.get('amount')
                    
                    #Check if the ingredient is in the bottle inventory
                    bottle = self.getBottle(ingredient.get('ingredient'))
                    if bottle:
                        ingredientDetails.setPosition(bottle.get('position'))
                        ingredientDetails.setType(bottle.get('type'))

                    self.ingredients_details.append(ingredientDetails)
                    
                self.db.insert_order(order, ingredients_dict)
                logging.info(f"Order added to the database")
                
                




    def getBottle(self, ingredient):
        # Details der Flasche aus der Konfiguration holen, inkl. Position und Typ
        for bottle in config.bottle_inventory:
            if bottle.get('name') == ingredient:
                msg = "Bottle: {0}, Position: {1}, Type: {2}".format(bottle.get('name'), bottle.get('position'), bottle.get('type'))
                #print('In getBottle: {0}'.format(msg))
                #logging.info(msg)
                return bottle 


class IngredientDetails():
    # This class is used to store the details of an ingredient
    def __init__(self, name=None, amount=None, unit=None):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.position = None
        self.type = None

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
        
    def setAmount(self, amount):
        self.amount = amount   

    def getAmount(self):
        return self.amount
        
    def setUnit(self, unit):
        self.unit = unit

    def getUnit(self):
        return self.unit
    
    def setPosition(self, position):
        self.position = position

    def getPosition(self):
        return self.position
    
    def setType(self, type):
        self.type = type

    def getType(self):  
        return self.type

    

        
            



            
