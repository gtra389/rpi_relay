#!/usr/bin/python
# -*- coding:utf-8 -*-
##################################################

#           P26 ----> Relay_Ch1
#	    P20 ----> Relay_Ch2
#	    P21 ----> Relay_Ch3

##################################################

import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time
app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   26 : {'name' : 'GPIO 26', 'state' : GPIO.HIGH},
   20 : {'name' : 'GPIO 20', 'state' : GPIO.HIGH},
   21 : {'name' : 'GPIO 21', 'state' : GPIO.HIGH}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)
print("Initiation is done.")
print("")

def init_relay():
    try:
        for pin in pins:
            GPIO.output(pin,GPIO.LOW)
            print("PIN {}:The Common Contact is access to the Normal Open Contact!".format(pin))            
            time.sleep(1)
            GPIO.output(pin,GPIO.HIGH)
            print("PIN {}:The Common Contact is access to the Normal Closed Contact!".format(pin))			
            time.sleep(1)
            print("Setup The Relay Module is done")
            print("-----------------------")	
    except:
		print("except")
		GPIO.cleanup()

def allNC_relay():
    for pin in pins:
		GPIO.output(pin,GPIO.HIGH)
		print("PIN {}:The Common Contact is access to the Normal Closed Contact!".format(ii+1))
		print("-----------------------")
		time.sleep(1)



@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " OFF."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " ON."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)

try:
    # init_relay()
    if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080, debug=True)
except KeyboardInterrupt:
	allNC_relay()
	print("Good bye.")
finally:
	GPIO.cleanup()
