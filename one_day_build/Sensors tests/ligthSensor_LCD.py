import time
import grovepi
from grove_rgb_lcd import *

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0

# Connect the LED to digital port D4
# SIG,NC,VCC,GND
led = 4

# Turn on LED once sensor exceeds threshold percentage
threshold = 10

# Set pins modes
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(led,"OUTPUT")

while True:
    # Get sensor value
    sensor_value = grovepi.analogRead(light_sensor)

    # Calculate percentage of light
    percentage = (float)(sensor_value) / 1023 * 100

    if percentage > threshold:
        # Send HIGH to switch on LED
        grovepi.digitalWrite(led,1)
        print("Led ON")
    else:
        # Send LOW to switch off LED
        grovepi.digitalWrite(led,0)
        print("Led OFF")

    print("Percentage = %.2f" %(percentage))

    # Set blackligth of the LCD
    setRGB(0,0,255)
    # Display ligth level on LCD
    setText("Light level:" + str(percentage))
    time.sleep(.5)