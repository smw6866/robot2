
import Robot
import RPi.GPIO as GPIO
import time
import random
import os

LEFT_TRIM   = 0
RIGHT_TRIM  = 0
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)


colors = [0x0000FF]
# pins = { 'pin_R':18, 'pin_G':12, 'pin_B':16 } #pins configured as dictionary 
pin_R = 12
pin_G = 32
pin_B = 36

ObstaclePin = 11
BuzzerPin = 16

GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location 
GPIO.setup(pin_R, GPIO.OUT) # Set pins' mode to output
GPIO.setup(pin_G, GPIO.OUT)
GPIO.setup(pin_B, GPIO.OUT)
GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BuzzerPin,GPIO.OUT)
#GPIO.output(BuzzerPin, GPIO.LOW)

#GPIO.output(pin_B, 0)
#GPIO.output(pin_R, 0)

#GPIO.output(pin_G, 1)
RIGHT = 15 # GPIO 22 pin 15 (Right side sensor)
LEFT = 13 # GPIO 27 pin 13 (Left side sensor)

GPIO.setup(RIGHT,GPIO.IN)
GPIO.setup(LEFT,GPIO.IN)

time.sleep(0.1)

def rightSensor():
	return GPIO.input(RIGHT)     # Getting readings from sensor on the right
def leftSensor():
	return GPIO.input(LEFT)      # Getting reading from sensor on the left 

def readSensor(id):
	tfile = open("/sys/bus/w1/devices/"+id+"/w1_slave")
	text = tfile.read()
	tfile.close()
	secondline = text.split ("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature= temperature / 1000
	print "Sensor: " + id + " - Current Temperature : %0.3f C" % temperature


# Reads temperature from all sensors found in /sys/bus/wl/devices
# starting  with "28-...

def readSensors():
	count = 0
	sensor = " "
	for file in os.listdir ("/sys/bus/w1/devices/"):
		if file.startswith("28-"):
			readSensor(file)
			count = 1
		elif count == 0:
			print "No sensor found! Check connection"


buzzerState = 0
# read temperature every second for all connected sensors
try:
        while True:
		if (0!= GPIO.input(ObstaclePin)):
			readSensors()
			GPIO.output(pin_G, 1)
			#GPIO.output(pin_R, 1)
			#GPIO.output(pin_B, 1)
			if rightSensor() == 1 and leftSensor() == 1:
                        	robot.forward(100)
                        	print("Both=1")
                	elif leftSensor() == 1 and rightSensor() == 0:
                        	robot.left(100)
                        	print("Left=1")
                	elif rightSensor() == 1 and leftSensor() == 0:
                        	robot.right(100)
                        	print("Right=1")
               		elif rightSensor() == 0 and leftSensor() == 0:
                        	robot.forward(100)
		if (0==GPIO.input(ObstaclePin)):
			startTime = time.time()
		while (0==GPIO.input(ObstaclePin)): 
			#GPIO.output(BuzzerPin, GPIO.HIGH)
			#time.sleep(1)
			#GPIO.output(BuzzerPin, GPIO.LOW)
			now = time.time()
			if (now-startTime) >= 5 and buzzerState != 1:
				buzzerState = 1
				print("Activating Buzzer")
				GPIO.output(BuzzerPin, GPIO.HIGH)
			GPIO.output(pin_G, 0)
			GPIO.output(pin_R, 1)
			robot.forward(0)
			robot.left(0)
			robot.right(0)
		GPIO.output(BuzzerPin, GPIO.LOW)
		buzzerState = 0
		GPIO.output(pin_G, 0)
		GPIO.output(pin_R, 0)
		GPIO.output(pin_B, 0)

except KeyboardInterrupt: 
        GPIO.cleanup()
