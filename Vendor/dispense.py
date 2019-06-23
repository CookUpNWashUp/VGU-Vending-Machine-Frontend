from gpiozero import LED
from django.conf import settings
from time import sleep

def dispense(slot):
    led = LED(slot)
    led.on()
    sleep(settings.TIME_TO_DISPENSE)
    led.off()
    
