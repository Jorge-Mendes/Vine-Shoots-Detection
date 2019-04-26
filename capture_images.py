#from getkey import getkey, keys
import sys
import glob
import os
import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

pin_greater = 32
pin_smaller = 36
pin_led = 37

GPIO.setup(pin_greater, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_smaller, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_led, GPIO.OUT)

clear = lambda: os.system('clear')
clear()

try:
	import picamera
except:
	print "\nCould not 'import picamera'!\nDummy files will be created!"

greater_than_10_images_path = "/home/pi/Desktop/Vine-Shoots-Detection/dataset/whole_images/greater_than_10/"
smaller_than_10_images_path = "/home/pi/Desktop/Vine-Shoots-Detection/dataset/whole_images/smaller_than_10/"
greater_than_10_images_class = "greater_than_10"
smaller_than_10_images_class = "smaller_than_10"
greater_than_10_last_image = 1
smaller_than_10_last_image = 1

def pin_greater_callback(a):
	GPIO.output(pin_led, GPIO.HIGH)
        print "Save image in >10cm class..."
        captureImage(greater_than_10_images_path, greater_than_10_images_class, greater_than_10_last_image)
        #greater_than_10_last_image += 1
        clear()
        verify_dataset()
	GPIO.output(pin_led, GPIO.LOW)

def pin_smaller_callback(a):
	GPIO.output(pin_led, GPIO.HIGH)
        print "Save image in <10cm class..."
	captureImage(smaller_than_10_images_path, smaller_than_10_images_class, smaller_than_10_last_image)
	#smaller_than_10_last_image += 1
	clear()
	verify_dataset()
	GPIO.output(pin_led, GPIO.LOW)

GPIO.add_event_detect(pin_greater, GPIO.FALLING, callback=pin_greater_callback, bouncetime=3000)
GPIO.add_event_detect(pin_smaller, GPIO.FALLING, callback=pin_smaller_callback, bouncetime=3000)


#=================================#
#=== GET THE LAST IMAGE NUMBER ===#
#=================================#
def verify_dataset():
	global greater_than_10_last_image
	global smaller_than_10_last_image
	greater_than_10_last_image = 1
	smaller_than_10_last_image = 1
	if greater_than_10_last_image <= 9:
		while glob.glob(greater_than_10_images_path + "greater_than_10__0000%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	if greater_than_10_last_image > 9 and greater_than_10_last_image <= 99:
		while glob.glob(greater_than_10_images_path + "greater_than_10__000%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	if greater_than_10_last_image > 99 and greater_than_10_last_image <= 999:
		while glob.glob(greater_than_10_images_path + "greater_than_10__00%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	if greater_than_10_last_image > 999 and greater_than_10_last_image <= 9999:
		while glob.glob(greater_than_10_images_path + "greater_than_10__0%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	if greater_than_10_last_image > 9999:
		while glob.glob(greater_than_10_images_path + "greater_than_10__%s.*" % greater_than_10_last_image):
			greater_than_10_last_image += 1
	print "\nNext greater_than_10 image:", greater_than_10_last_image

	if smaller_than_10_last_image <= 9:
		while glob.glob(smaller_than_10_images_path + "smaller_than_10__0000%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	if smaller_than_10_last_image > 9 and smaller_than_10_last_image <= 99:
		while glob.glob(smaller_than_10_images_path + "smaller_than_10__000%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	if smaller_than_10_last_image > 99 and smaller_than_10_last_image <= 999:
		while glob.glob(smaller_than_10_images_path + "smaller_than_10__00%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	if smaller_than_10_last_image > 999 and smaller_than_10_last_image <= 9999:
		while glob.glob(smaller_than_10_images_path + "smaller_than_10__0%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	if smaller_than_10_last_image > 9999:
		while glob.glob(smaller_than_10_images_path + "smaller_than_10__%s.*" % smaller_than_10_last_image):
			smaller_than_10_last_image += 1
	print "Next smaller_than_10 image:", smaller_than_10_last_image

	print "\nPress:\n\tDOWN to save image in <10cm class\n\tUP to save image in >10cm class\n\tESC to exit\n"
	print "Press a key..."

#=================================#
#========= CAPTURE IMAGE =========#
#=================================#
def captureImage(image_path, image_class, image_numb):
	# Generate the picture's name
	if image_numb <= 9:
		image_name = str(image_class) + "__0000" + str(image_numb) + ".jpg"
	if image_numb > 9 and image_numb <= 99:
		image_name = str(image_class) + "__000" + str(image_numb) + ".jpg"
	if image_numb > 99 and image_numb <= 999:
		image_name = str(image_class) + "__00" + str(image_numb) + ".jpg"
	if image_numb > 999 and image_numb <= 9999:
		image_name = str(image_class) + "__0" + str(image_numb) + ".jpg"
	if image_numb > 9999:
		image_name = str(image_class) + "__" + str(image_numb) + ".jpg"
	final_path = image_path + image_name

	try:
		with picamera.PiCamera() as camera:
			camera.resolution = (2592, 1944)        # 5MP (Camera Module v1)
			#camera.resolution = (3280, 2464)        # 8MP (Camera Module v2)
			#camera.rotation = 180
			#camera.saturation = 0
			#camera.brightness = 50
			camera.capture(final_path)
	except:
		# Create a dummy file
		dummy_file = open(final_path, "w")
		time.sleep(1)
		dummy_file.close()


#################################
############# START #############
#################################
verify_dataset()
while True:
        time.sleep(0.5)
        #pass
	#key = getkey()
	#if key == keys.DOWN:
	#	print "Save image in <10cm class..."
	#	captureImage(smaller_than_10_images_path, smaller_than_10_images_class, smaller_than_10_last_image)
	#	#smaller_than_10_last_image += 1
	#	clear()
	#	verify_dataset()
	#elif key == keys.UP:
	#	print "Save image in >10cm class..."
	#	captureImage(greater_than_10_images_path, greater_than_10_images_class, greater_than_10_last_image)
	#	#greater_than_10_last_image += 1
	#	clear()
	#	verify_dataset()
	#elif key == keys.ESC:
	#	print "ESC key pressed... Exit the script!\n"
	#	sys.exit()
	#else:
	#	print "Wrong key pressed!\n\nPress a key..."
	#	#pass

