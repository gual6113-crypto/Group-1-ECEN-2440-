"""
Lab 15 - DRV8835 single-motor test (Raspberry Pi Pico, MicroPython)

Drives Motor A through the DRV8835 in PHASE/ENABLE mode (MODE pin = HIGH):
  APH = direction (GPIO high/low)
  AEN = speed (PWM duty cycle)

Steps through direction and duty cycle with long pauses so you have
time to capture scope traces and read the multimeter at each state.
"""

from machine import Pin, PWM
from time import sleep

# ---------------------------------------------------------------
# PIN ASSIGNMENTS -- CHANGE THESE TO MATCH YOUR WIRING (GP numbers)
# ---------------------------------------------------------------
AEN_PIN = 2    # Motor A enable (PWM) -> DRV8835 AENABLE (aen1)
APH_PIN = 3    # Motor A phase (dir)  -> DRV8835 APHASE  (aph1)
MODE_PIN = 6   # DRV8835 MODE pin; set to None if MODE is wired to 3.3V

PWM_FREQ = 20000                 # 20 kHz, above audible range
HOLD_TIME = 5                    # seconds per state (time to measure)
DUTY_STEPS = [25, 50, 75, 100]   # percent

# ---------------------------------------------------------------
# Setup
# ---------------------------------------------------------------
if MODE_PIN is not None:
    mode = Pin(MODE_PIN, Pin.OUT)
    mode.value(1)  # HIGH = PHASE/ENABLE mode

aph = Pin(APH_PIN, Pin.OUT)
aen = PWM(Pin(AEN_PIN))
aen.freq(PWM_FREQ)
aen.duty_u16(0)


def set_duty(percent):
    """Set Motor A PWM duty cycle from 0-100 percent."""
    aen.duty_u16(int(percent / 100 * 65535))


def run(direction, percent):
    """direction: 1 = PHASE high, 0 = PHASE low."""
    aph.value(direction)
    set_duty(percent)
    print("PHASE={} | duty={}%".format(direction, percent))
    sleep(HOLD_TIME)


# ---------------------------------------------------------------
# Main test sequence
# ---------------------------------------------------------------
try:
    print("=== DRV8835 single-motor test starting ===")
    set_duty(0)
    print("IDLE (0% duty) - baseline")
    sleep(HOLD_TIME)

    for direction in (1, 0):
        for percent in DUTY_STEPS:
            run(direction, percent)
        print("STOP (0% duty) - capture direction-change behavior")
        set_duty(0)
        sleep(HOLD_TIME)

    print("=== Test complete ===")

finally:
    set_duty(0)
    print("Motor stopped.")
