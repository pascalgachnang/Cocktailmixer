import kivy
import logging
import time
import drinkprocessor
import os
from kivy.app import App
from kivy.uix.widget import Widget  
from kivy.uix.button import Button  
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from StepperMotor.StepperMotor import StepperMotor
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage



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

class PositioningWindow(Screen): #Layout for the positioning window
    pass

class MainWindow1(Screen): #Layout for the main window, first page
    pass

class MainWindow2(Screen): #Layout for the main window, second page
    pass

class MainWindow3(Screen):
    pass

class DrinkInProgress(Screen): #Layout for the drink in progress window
    pass
    
class WindowManager(ScreenManager):
    pass

# Load the kv file
kv = Builder.load_file("my.kv")

class MyCocktailmixerApp(App):
    def build(self):
        self.image_cache = {}  # We store the images in a cache to avoid loading them multiple times
        self.custom_dispatcher = CustomEventDispatcher()    
        self.drinkprocessor = drinkprocessor.OrderQueue(self)   # Hier übergeben wir die App Instanz an den OrderQueue
        self.drinkprocessor.start()
        self.lastclicktime = None
        self.steppermotor = StepperMotor()
        self.instance = None
        self.current_screen = None
        
        # Listen for the custom event
        self.custom_dispatcher.bind(on_custom_action=self.on_custom_action)
        #self.preload_images()

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

        if self.lastclicktime is not None:  # Ignore rapid clicks
            if time.time() - self.lastclicktime < 2:
                logging.info("Ignoring rapid clicks")
                return
        self.lastclicktime = time.time()
        logging.info("Incoming DrinkOrder")
        
        # search for a recipe
        self.recipe = drinkprocessor.Recipe(search_string=instance.text)

        # add an order to the order queue
        self.drinkprocessor.addOrder(self.recipe)



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
        

    
    


