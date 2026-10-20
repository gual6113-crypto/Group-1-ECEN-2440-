import time
from machine import PWM, Pin

TX_PIN = 17
ir_pwm = PWM(Pin(TX_PIN))
ir_pwm.freq(38000)

print("IR Transmitter started. Sending pulses...")

try:
  while True:
    ir_pwm.duty_u16(21845)
    print("Transmitting...")
    time.sleep_ms(10)

    ir_pwm.duty_u16(0)
    print("Transmitting stopped.")
    time.sleep_ms(50)

except KeyboardInterrupt:
  ir_pwm.duty_u16(0)
  ir_pwm.deinit()
  print("Keyboard interrupt, transmission end.")

# Temp as of 10/19
