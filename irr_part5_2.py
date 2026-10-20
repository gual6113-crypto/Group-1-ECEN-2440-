import time
from machine import Pin

RX_PIN = 14  # Connected to TSOP Data Out pin
LED1_PIN = 16  # User LED 1
LED2_PIN = 18  # User LED 2
LED3_PIN = 19  # User LED 3

rx = Pin(RX_PIN, Pin.IN, Pin.PULL_UP)
leds = [
    Pin(LED1_PIN, Pin.OUT),
    Pin(LED2_PIN, Pin.OUT),
    Pin(LED3_PIN, Pin.OUT),
]
def set_user_leds(state):
  val = 1 if state else 0
  for led in leds:
    led.value(val)

print("--- IR Receiver Serial Monitor ---")
print("Listening on GP{}, driving LEDs on GP{}, {}, {}".format(
    RX_PIN, LED1_PIN, LED2_PIN, LED3_PIN
))
last_val = rx.value()

while True:
  current_val = rx.value()
  if current_val == 0:
    set_user_leds(True)
    if last_val != 0:
      print("RX: SIGNAL DETECTED -> User LEDs ON")
  else:
    set_user_leds(False)
    if last_val != 1:
      print("RX: IDLE (No Signal) -> User LEDs OFF")

  last_val = current_val
  time.sleep_ms(2)

# temp as of 10/19
