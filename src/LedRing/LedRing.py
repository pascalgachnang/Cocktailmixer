import time
import board
import neopixel

import time
import board
import neopixel

class LedRing():

    def __init__(self):
        # Konfiguration der LED
        LED_COUNT = 16        # Anzahl der LEDs in Ihrem LED-Ring
        LED_PIN = board.D26   # GPIO-Pin, an den der LED-Ring angeschlossen ist
        LED_ORDER = neopixel.RGB   # LED-Reihenfolge (abhängig von Ihrem LED-Ring)

        # Initialisierung des LED-Rings
        self.pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, auto_write=False, pixel_order=LED_ORDER)

    # Funktion zum Ändern der Farbe aller LEDs
    def set_color(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    
