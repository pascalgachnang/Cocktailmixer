import kivy
import logging
import time
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

#Layouts for the windows
class PasswordWindow(Screen): #Layout for the password window
    pass

class PositioningWindow(Screen): #Layout for the positioning window
    def btn_positioning(self):
        show_popup_positioning()

    def btn_positioning_complete(self):
        show_popup_positioning_complete()

class MainWindow1(Screen): #Layout for the main window, first page
    pass

class MainWindow2(Screen): #Layout for the main window, second page
    pass

class WindowManager(ScreenManager):
    pass


#Layouts for the popup windows
class P_Positioning(FloatLayout): #Layout for the positioning popup window
    pass

class P_PositioningComplete(FloatLayout): #Layout for the positioning complete popup window
    pass


#Functions for the popup windows
def show_popup_positioning():
    show = P_Positioning()

    popupWindow_Positioning = Popup(title="Popup Window", content=show, size_hint=(None,None), size=(400,400))

    popupWindow_Positioning.open()

def show_popup_positioning_complete():
    show = P_PositioningComplete()

    popupWindow_PositioningComplete = Popup(title="Popup Window", content=show, size_hint=(None,None), size=(400,400))

    popupWindow_PositioningComplete.open()



kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv 
    


