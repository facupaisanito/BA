# =================================================================================
# =================================================================================
# Filename: scriptTest1.pyplot
# Author: Ignacio Cazzasa
# Date created: May 15, 2018
# Date modified: May 16, 2018
# Description: Dummy script, alternate between CHARGE and DISCHARGE profile before
# ending in STOP,NTF.
# Shows the way to intercharge data between the GUI and SCRIPT. Use the sharedMemory
# file to store sta between sessions.
# =================================================================================
# =================================================================================

import sys
import csv
import operator
import numbers
import random
import ConfigParser
#SOLO TEST: para graficar senal
#import numpy as np
#import matplotlib.pyplot as plt


arg_num=len(sys.argv)
if(arg_num==2) :
	station=sys.argv[1]

	#Get the stored memory information
	storedMemory = ConfigParser.SafeConfigParser()
	storedMemory.read("data/st"+station+".ini")
	entradas = storedMemory.getint('General','entradas')
	storedMemory.set('General','entradas',str(entradas+1))

	if entradas == 5 :
		storedMemory.set('GUI','line1','"Analysis Finished - NTF"')
		storedMemory.set('GUI','line2','"Health: 68/100    Internal Z: 52mOhm"')
		storedMemory.set('GUI','bgcolor','"244,123,183"')
		storedMemory.set('GUI','extra_info','"Donec eu ultricies sem. Proin ut dictum lacus. Vestibulum cursus ipsum eget sem condimentum feugiat id ac arcu. Proin semper nulla sed metus mattis, et euismod mauris iaculis."')
		print "STOP,NTF,68,52"
	else :
		if entradas % 2 == 0:
			# Even 
			print "CHARGE"
		else:
			# Odd
			print "DISCHARGE"
		
		
	# Writing memory to 'stX.ini' file
	with open('data/st1.ini', 'w') as configfile:
		storedMemory.write(configfile)
	
sys.exit()
