import logging
import config




class OrderQueue():

    def __init__(self):
        self.order_queue = []

    def setOrderQueue(self, order_queue):
        self.order_queue = order_queue

    def getOrderQueue(self):
        return self.order_queue
    
    def addOrder(self, order):
        # pass in a recipe object
        order = Order(order) 
        self.order_queue.append(order)

    def removeOrder(self, order):
        self.order_queue.remove(order)

    def clearOrderQueue(self):
        self.order_queue = []

    def printOrderQueue(self):
        for order in self.order_queue:
            print("Order: {0}".format(order.get('name')))

    def processOrderQueue(self):
        for order in self.order_queue:
            print("Order: {0}".format(order.get('name')))

            self.processOrder(order)

    def processOrder(self, order):
        print("Order: {0}".format(order.get('name')))

        dp = DrinkProcessor(search_string=order.get('name'))

    

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


class DrinkProcessor():
     
    def __init__(self, search_string=None):
        if search_string is None:
            return None
        else:
            recipe = Recipe(search_string=search_string)
            order_queue.append(recipe)

    


class Recipe():

    def __init__(self, search_string=None):
        
        self.search_string = search_string
        self.recipe = None
        self.findRecipes()


    def findRecipes(self):
        logging.info("Reading recipes")
        
        for recipe in config.recipes:
            if recipe.get('name') == self.search_string:
                msg = "Rezept: {0}, Anzahl: {1}".format(recipe.get('name'), len(config.recipes))
                logging.info(msg)
                self.recipe = recipe
                for ingredient in recipe.get('ingredients'):
                    msg = "Ingedient: {0}, Menge: {1}, Unit: {2}".format(ingredient.get('ingredient'), ingredient.get('amount'), ingredient.get('unit'))
                    logging.info(msg)

        
            



            
