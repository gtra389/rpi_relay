##################################################

#           P26 ----> Relay_Ch1
#			P20 ----> Relay_Ch2
#			P21 ----> Relay_Ch3

##################################################
#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

#GPIO Pin
Relay = [26, 20, 21]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for ii in range(3):
    GPIO.setup(Relay[ii], GPIO.OUT)
    GPIO.output(Relay[ii], GPIO.HIGH)
print("Initiation is done.")
print("")


def init_relay():
    try:
		for ii in range(3):
			GPIO.output(Relay[ii],GPIO.LOW)
			print("Channel {}:The Common Contact is access to the Normal Open Contact!".format(ii+1))
			time.sleep(1)
			GPIO.output(Relay[ii],GPIO.HIGH)
			print("Channel {}:The Common Contact is access to the Normal Closed Contact!".format(ii+1))
			print("-----------------------")
			time.sleep(1)
		print("Setup The Relay Module is done")	
	except:
		print("except")
		GPIO.cleanup()

def allNC_relay():
    for ii in range(3):
		GPIO.output(Relay[ii],GPIO.HIGH)
		print("Channel {}:The Common Contact is access to the Normal Closed Contact!".format(ii+1))
		print("-----------------------")
		time.sleep(1)



def select_relay():
    flag_1 = True
	flag_2 = True
	flag_3 = True

	try:
		while True:
			relayNum = input("Please enter the number of relay[1-3].")  		
				if (relayNum == 1):
					if (flag_1):
						GPIO.output(Relay[relayNum-1],GPIO.LOW)
						print("Channel {}:The Common Contact is access to the Normal Open Contact!".format(relayNum))
						flag_1 = not flag_1
					else:
						GPIO.output(Relay[relayNum-1],GPIO.High)
						print("Channel {}:The Common Contact is access to the Normal Closed Contact!".format(relayNum))
						flag_1 = not flag_1
				elif (relayNum == 2):
					if (flag_2):
						GPIO.output(Relay[relayNum-1],GPIO.LOW)
						print("Channel {}:The Common Contact is access to the Normal Open Contact!".format(relayNum))
						flag_2 = not flag_2
					else:
						GPIO.output(Relay[relayNum-1],GPIO.High)
						print("Channel {}:The Common Contact is access to the Normal Closed Contact!".format(relayNum))
						flag_2 = not flag_2
				elif (relayNum == 3):
					if (flag_3):
						GPIO.output(Relay[relayNum-1],GPIO.LOW)
						print("Channel {}:The Common Contact is access to the Normal Open Contact!".format(relayNum))
						flag_3 = not flag_3
					else:
						GPIO.output(Relay[relayNum-1],GPIO.High)
						print("Channel {}:The Common Contact is access to the Normal Closed Contact!".format(relayNum))
						flag_3 = not flag_3
				else:
					print("No such name, please try again")
	except:
		allNC_relay()
		print("Good bye.")

init_relay()
init_relay()

    				
			


			







