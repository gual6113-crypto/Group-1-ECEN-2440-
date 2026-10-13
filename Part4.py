

import machine
from time import sleep
from machine import Pin, PWM
from machine import Pin

Pin10 = Pin(10, Pin.OUT)
Pwm11 = PWM(Pin(11))
Pin12 = Pin(12, Pin.OUT)
Pwm13 = PWM(Pin(13))

Pin10.value(1)            #Make the pin high to set the direction of the motor
Pwm11.freq(1000)          #Set the frequency and duty cycle of the PWM signal that controls the speed of the motor
Pwm11.duty_u16(5000)

Pin12.value(1)            #Make the pin high to set the direction of the motor
Pwm13.freq(1000)          #Set the frequency and duty cycle of the PWM signal that controls the speed of the motor
Pwm13.duty_u16(5000)

# while True:                    
#     Pin10.value(1)
#     Pin12.value(1)
#     print("Motor Forward")
#     sleep(1)
#     Pin10.value(0)
#     Pin12.value(0)
#     print("Motor Reverse")
#     sleep(1)

while True:
    sleep(0.1)