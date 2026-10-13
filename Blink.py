from machine import Pin
from time import sleep

# Connect LEDs to GPIO 16, 17, and 18 (with suitable current-limiting resistors).
leds = [Pin(pin, Pin.OUT) for pin in (16, 17, 18)]

while True:
    for led in leds:
        led.on()
        sleep(0.5)
        led.off()
