from machine import Pin, PWM, I2C

Pin10 = Pin(10, Pin.OUT)
Pwm11 = PWM(Pin(11))
Pin12 = Pin(12, Pin.OUT)
Pwm13 = PWM(Pin(13))

MOTOR_DUTY = 20000

def motors_on():
 Pin10.value(1)            #Make the pin high to set the direction of the motor
 Pwm11.freq(1000)          #Set the frequency and duty cycle of the PWM signal that controls the speed of the motor
 Pwm11.duty_u16(MOTOR_DUTY)

 Pin12.value(1)            #Make the pin high to set the direction of the motor
 Pwm13.freq(1000)          #Set the frequency and duty cycle of the PWM signal that controls the speed of the motor
 Pwm13.duty_u16(MOTOR_DUTY)

def motors_off():
 Pwm11.duty_u16(0)
 Pwm13.duty_u16(0)
 Pin10.value(0)
 Pin12.value(0)

# ------------------------------------------------------------------------------------------------------------------

from ir_rx.nec import NEC_8 # Use the NEC 8-bit class
from ir_rx.print_error import print_error # for debugging
# Callback function to execute when an IR code is received
def ir_callback(data, addr, _):
    print(f"Received NEC command! Data: 0x{data:02X}, Addr: 0x{addr:02X}")
# Setup the IR receiver
ir_pin = Pin(18, Pin.IN, Pin.PULL_UP) # Adjust the pin number based on your wiring

ir_receiver = NEC_8(ir_pin, callback=ir_callback)
# Optional: Use the print_error function for debugging
ir_receiver.error_function(print_error)

#---------------------------------------------------------------------------------------------------------------------

import seesaw
import time
# Initialize I2C. Adjust pin numbers based on your Pico's configuration
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
# Initialize the Seesaw driver with the I2C interface
# Use the Gamepad QT's I2C address from the Arduino code (0x50)
seesaw_device = seesaw.Seesaw(i2c, addr=0x50)
# Define button and joystick pin numbers as per the Arduino code
BUTTON_A = 5
BUTTON_B = 1
BUTTON_X = 6
BUTTON_Y = 2
BUTTON_START = 16
BUTTON_SELECT = 0
JOYSTICK_X_PIN = 14
JOYSTICK_Y_PIN = 15
# Button mask based on Arduino code
BUTTONS_MASK = (1 << BUTTON_X) | (1 << BUTTON_Y) | (1 << BUTTON_A) | (1 << BUTTON_B) | (1 << BUTTON_SELECT) | (1 << BUTTON_START)

# Define LED pins
LED_1_PIN = 28
LED_2_PIN = 27
LED_3_PIN = 26
LED_4_PIN = 22
LED_1 = Pin(LED_1_PIN, Pin.OUT)
LED_2 = Pin(LED_2_PIN, Pin.OUT)
LED_3 = Pin(LED_3_PIN, Pin.OUT)
LED_4 = Pin(LED_4_PIN, Pin.OUT)
# Initialize LED states
led_states = {
 BUTTON_A: False,
 BUTTON_B: False,
 BUTTON_X: False,
 BUTTON_Y: False,
 BUTTON_START: False,
 BUTTON_SELECT: False
}
# Initialize last button states
last_buttons = BUTTONS_MASK
# Initialize joystick center position
joystick_center_x = 511
joystick_center_y = 497
def setup_buttons():
 """Configure the pin modes for buttons."""
 seesaw_device.pin_mode_bulk(BUTTONS_MASK, seesaw_device.INPUT_PULLUP)
def read_buttons():
 """Read and return the state of each button."""
 return seesaw_device.digital_read_bulk(BUTTONS_MASK)
def read_joystick_x():
 return 1023 - seesaw_device.analog_read(JOYSTICK_X_PIN)
def read_joystick_y():
 return seesaw_device.analog_read(JOYSTICK_Y_PIN)
def set_led(pin, state):
 """Turn the LED connected to the given pin on or off."""
 pin.value(state)
def handle_button_press(button):
 """Toggle the corresponding LED state on button press."""
 global led_states
 led_states[button] = not led_states[button]
 print("Button", button, "pressed, LED toggled", "on" if led_states[button] else "off")
def main():
 """Main program loop."""
 global last_buttons # Ensure last_buttons is recognized as a global variable
 global joystick_center_x, joystick_center_y
 setup_buttons()
 motors_on()
 last_buttons = read_buttons()
 joystick_center_x = read_joystick_x()
 joystick_center_y = read_joystick_y()
 last_x, last_y = joystick_center_x, joystick_center_y
 joystick_threshold = 50 # Adjust threshold as needed
 try:
  while True:
    current_buttons = read_buttons()
 # Check if button state has changed
    for button in led_states:
        pressed_now = not (current_buttons & (1 << button))
        was_pressed = not (last_buttons & (1 << button))
        if pressed_now and not was_pressed:
            handle_button_press(button)
 # Read joystick values
    current_x = read_joystick_x()
    current_y = read_joystick_y()
 # Check if joystick position has changed significantly
    if abs(current_x - last_x) > joystick_threshold or abs(current_y - last_y) > joystick_threshold:
        print("Joystick moved - X:", current_x, ", Y:", current_y)
        last_x, last_y = current_x, current_y
 # Determine which LED to turn on based on joystick direction
    joy_up = current_y < joystick_center_y - joystick_threshold
    joy_down = current_y > joystick_center_y + joystick_threshold
    joy_left = current_x < joystick_center_x - joystick_threshold
    joy_right = current_x > joystick_center_x + joystick_threshold
    set_led(LED_1, led_states[BUTTON_A] or joy_up)
    set_led(LED_2, led_states[BUTTON_B] or joy_down)
    set_led(LED_3, led_states[BUTTON_X] or joy_left)
    set_led(LED_4, led_states[BUTTON_Y] or joy_right)
    last_buttons = current_buttons
    time.sleep(0.05) # Delay to prevent overwhelming the output
 finally:
  motors_off()
  set_led(LED_1, False)
  set_led(LED_2, False)
  set_led(LED_3, False)
  set_led(LED_4, False)
if __name__ == "__main__":
 main()