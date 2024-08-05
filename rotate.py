import RPi.GPIO as GPIO
import time
import os

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define servo pins. These pins correlate the to the GPIO pins on the raspberry pi. 
# Here is an image showing the GPIO pins: https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png?hash=df7d7847c57a1ca6d5b2617695de6d46
SERVO_1_PIN = 11
SERVO_2_PIN = 12

# Set up servo pins as outputs; meaning it is sending signals out rather than receiving messages. 
GPIO.setup(SERVO_1_PIN, GPIO.OUT)
GPIO.setup(SERVO_2_PIN, GPIO.OUT)

# Create PWM objects for each servo (50Hz frequency is just default)
pwm1 = GPIO.PWM(SERVO_1_PIN, 50)
pwm2 = GPIO.PWM(SERVO_2_PIN, 50)

# Start PWM
pwm1.start(0)
pwm2.start(0)

def set_speed(pwm, speed):
    """Set speed from -100 to 100. Backwards is -100; forward is 100."""
    duty = 7.5 + (speed / 20)
    pwm.ChangeDutyCycle(duty)

def read_command():
    if os.path.exists('servo_commands.txt'):
        with open('servo_commands.txt', 'r') as file:
            return file.read().strip()
    return '0 0'

try:
    while True:
        command = read_command()
        servo1_speed, servo2_speed = map(int, command.split())
        
        print(f"Setting Servo 1 speed to {servo1_speed}")
        set_speed(pwm1, servo1_speed)
        
        print(f"Setting Servo 2 speed to {servo2_speed}")
        set_speed(pwm2, servo2_speed)
        
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

except KeyboardInterrupt:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
    print("Stopped")