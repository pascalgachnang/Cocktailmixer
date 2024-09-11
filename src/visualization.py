import kivy
import logging
import time
import drinkprocessor
import os
import sys
import config
from kivy.app import App
from kivy.uix.widget import Widget  
from kivy.uix.button import Button  
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from StepperMotor.StepperMotor import StepperMotor
from RelayBoard.RelayBoard import RelayBoard
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.properties import StringProperty
from pprint import pprint
from kivy.factory import Factory



class CustomEventDispatcher(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_custom_action')
        super(CustomEventDispatcher, self).__init__(**kwargs)

    def do_custom_action(self, *args):
        # when do_something is called, the 'on_test' event will be
        # dispatched with the value
        logging.info(f"in do_custom_action: {args[0]}")
        self.dispatch('on_custom_action', args[0])

    def on_custom_action(self,  *args):
        logging.info(f"in on_custom_action: {args}")



class MyLayout(Widget):
    pass

#Layouts for the windows

class P_StartMixing(Popup):
    def refresh_ingredients_label(self, ingredients_text):
        # Refresh the ingredients label with the new text
        self.ids.ingredients_label.text = ingredients_text

    def refresh_garnish_label(self, garnish_text):
        # Refresh the garnish label with the new text
        self.ids.garnish_label.text = garnish_text

    def refresh_titel(self, title_text):
        # Refresh the title of the popup
        self.title = title_text


class PositioningWindow(Screen): #Layout for the positioning window
    pass

class MainWindow1(Screen): #Layout for the main window, first page
    pass

class MainWindow2(Screen): #Layout for the main window, second page
    pass

class MainWindow3(Screen):
    pass

class MainWindow4(Screen): #Layout for the main window, fourth page (test page)
    pass


class DrinkInProgress(Screen): #Layout for the drink in progress window
    pass
    
class WindowManager(ScreenManager):
    pass

# Load the kv file
kv = Builder.load_file("my.kv")

class MyCocktailmixerApp(App):

    def __init__(self, **kwargs):
        super(MyCocktailmixerApp, self).__init__(**kwargs)
        self.image_cache = {}
        self.custom_dispatcher = CustomEventDispatcher()
        self.drinkprocessor = drinkprocessor.OrderQueue(self)
        self.drinkprocessor.start()
        self.lastclicktime = None
        self.steppermotor = StepperMotor()
        self.relayb = None
        self.instance = None
        self.current_screen = None
        self.dynamic_text = StringProperty("Hello, Mixing Jenny!")
        self.popup = None

    def build(self):
        return kv 
    
    
    
    def on_button_press(self, instance):
        # Access the instance of the pressed button
        logging.info(f"Button pressed: {instance.text}")
        print(f"Button pressed: {instance.text}")
        instance.background_color = (0, 1, 0, 1)
        instance.text = "TEST"

    
    def IncomingDrinkOrder(self, instance):

        self.instance = instance    # We store the instance of the button that was pressed
        logging.info(f"Button pressed: {instance.text}, {instance.__dict__}")

        self.current_screen = self.root.current   # We store the current screen to switch back to it after the drink is done
        logging.info(f"Current screen: {self.current_screen}")  

        

    def AddOrder(self):
        # add an order to the order queue
        if self.lastclicktime is not None:  # Ignore rapid clicks
            if time.time() - self.lastclicktime < 2:
                logging.info("Ignoring rapid clicks")
                return
        self.lastclicktime = time.time()
        
        # search for a recipe
        self.recipe = drinkprocessor.Recipe(search_string=self.instance.text)
        logging.info(f"Recipe: {self.recipe}")

        self.drinkprocessor.addOrder(self.recipe)
        logging.info(f"Order added to the queue")
        logging.info(f"Recipe: {self.recipe}")
        
    def show_popup(self, dt=None):
    # Build the popup
        if self.popup and self.popup._is_open:
            logging.info("Popup is already open.")
            return

        self.popup = Factory.P_StartMixing()

        # Open popup with delay
        Clock.schedule_once(lambda dt: self.popup.open(), 0.2)
        
   

    def update_ingredients_label(self, *args):
        # Get the ingredients for the recipe
        if not hasattr(self, 'instance') or not self.instance:
            logging.error("Instance is not available.")
            return

        recipe_name = self.instance.text
        logging.info(f"Searching for recipe with name: {recipe_name}")

        # Search for the recipe
        for recipe in config.recipes:
            if recipe.get('name') == recipe_name:
                logging.info(f"Recipe found: {recipe.get('name')}")

                # Get the ingredients
                ingredients = recipe.get('ingredients', [])
                ingredients_text = "[b]Ingredients:[/b]\n"
                for ingredient in ingredients:
                    ingredient_name = ingredient.get('ingredient')
                    amount = ingredient.get('amount')
                    unit = ingredient.get('unit')

                    # Are there any special ingredients?
                    if ingredient_name in ['Zuckersirup', 'Grenadinesaft', 'Mandelsirup']:
                        msg = f"{ingredient_name}: {amount} {unit} (to be added manually)\n"
                    else:
                        msg = f"{ingredient_name}: {amount} {unit}\n"

                            # Add special ingredients
                    special = ingredient.get('special')
                    if special:
                        msg = f"{special}\n"

                    
                    ingredients_text += msg
                
                # Check if there is a garnish
                garnish = recipe.get('garnish')
                garnish_text = ""
                if garnish:
                    garnish_text += f"[b]Garnish:[/b]\n{garnish}\n"

                logging.info(ingredients_text)
                logging.info(garnish_text)

                # Show the popup
                self.show_popup()
                
                # Refresh the ingredients label
                self.popup.refresh_ingredients_label(ingredients_text)
                self.popup.refresh_garnish_label(garnish_text)
                self.popup.refresh_titel(recipe_name)
                return

        logging.info(f"Recipe not found for name: {recipe_name}")
        
    def calling_reference_run(self):
        # Call the reference run of the stepper motor
        logging.info("Calling reference run")

        self.steppermotor.reference_run()



    def on_custom_action(self, *args):
        # This is the method that is called when the custom event is dispatched

        logging.info(f"I am dispatched {args[1]} ID: {self.instance}")

        data = args[1]
        """
        # switch to the drink in progress screen and back to the main window
        if data == 1:
            screen = "drink in progress"
            #self.switchScreens(screen)
            self.instance.background_color = (0, 1, 0, 1)
            #self.instance.text = "START"
        elif data == 0:
            #self.switchScreens(self.current_screen)
            #self.instance.text = "DONE"
            self.instance.background_color = (0, 1, 0, 0)  # green colour transparent
        """

    def switchScreens(self, screen):
        self.root.current = screen

    def runPump(self, instance):
        # This triggers the corresponding pump to RUN for venting the hose
        logging.info(f"Pump pressed  {instance.text} Instance: {instance.__dict__}")

        self.instance = instance    # We store the instance of the button that was pressed

        amount_ingredient = 1 # defaults to 1
        ingredient_name = instance.text # Take the name of the buttons

        logging.info(f"Pump {instance.text} Ingredient: {ingredient_name} Amount: {amount_ingredient}")

        # Ingredient takes also Pumpe 1 - 4, according to the pump switches!
        self.relayb = RelayBoard(amount_ingredient, ingredient_name)
        self.relayb.start()
        #self.relayb.join()

    def stopPump(self, instance):
        # This triggers the corresponding pump to STOP for venting the hose
        logging.info(f"Pump released {instance.text} Instance: {instance.__dict__}")

        self.relayb.setEvent()




    def update_text(self, *args):
        # Update the value of the dynamic text -> Referenz zum Text Label geht nicht!
        logging.info(f"Self: {self} ID: {self.instance}")
        logging.info(f"Button pressed: {self.dynamic_text}")
        self.dynamic_text = "Bye, Mixing Jenny!"
        logging.info(f"Button pressed: {self.dynamic_text}")        

    def terminateMixingJenny(self, instance, title=None, message=None):
        # Terminate the program
        logging.info(f"Button pressed: {instance} title: {title} message: {message}")
        self.messageBox(instance, title, message)

        logging.info(f"Jenny is exiting. Bye!")
        os._exit(0)
    
    def messageBox(self, instance, title=None, message=None):
        layout = GridLayout(cols=1)
        lbl = Label(text=message)
        cancelButton = Button(text="Cancel")
        okButton = Button(text="OK")
        layout.add_widget(lbl)
        layout.add_widget(cancelButton)
        layout.add_widget(okButton)

        self.popup = Popup(
            title=title, content=layout,
            auto_dismiss=False, size_hint=(None, None),
            size=(400, 400)
        )

        self.popup.open()
        cancelButton.bind(on_press=self.on_close)
        okButton.bind(on_press=self.on_ok)
        
   
    def on_close(self, event):
        self.popup.dismiss()
        return False

    def on_ok(self, event):
        self.popup.dismiss()
        return True