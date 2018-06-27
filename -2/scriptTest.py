# =================================================================================
# =================================================================================
# Filename: scriptTest2.pyplot
# Author: Ignacio Cazzasa
# Date created: May 16, 2018
# Date modified: May 16, 2018
# Description: 
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

#Machine Status
initState = "initState"
initDischarge = "initDischarge"
initCharge = "initCharge"
measureZ = "measureZ"
rest1 = "rest1"

#Umbral voltages
umbralVoltHigh = 3800
umbralVoltMin = 3600
umbralVoltLow = 3200


arg_num=len(sys.argv)
if(arg_num==2) :
	station=sys.argv[1]

	#Get the stored memory information
	storedMemory = ConfigParser.SafeConfigParser()
	storedMemory.read("data/st"+station+".ini")
	entradas = storedMemory.getint('General','entradas')
	machineStatus = storedMemory.get('General','machineStatus')
	storedMemory.set('General','entradas',str(entradas+1))
	
	#Set the correct state machine status
	if entradas == 0 :
		machineStatus = initState
		storedMemory.set('General','machineStatus',machineStatus)

	#Open the waveform
	file_name = "data/st"+station+".csv"
	with open (file_name,'rb') as f:
		reader_evaluar=csv.reader(f)
		file_evaluar=list(reader_evaluar)
		file_evaluar.pop(0) #elimino el primer renglon con el titulo
		file_evaluar.pop(0) #elimino el segundo renglon con info
		file_evaluar.pop(0) #elimino el tercer renglon con info
		statusVector=map(operator.itemgetter(0),file_evaluar)
		timeVector=map(operator.itemgetter(1),file_evaluar)
		voltageVector=map(operator.itemgetter(2),file_evaluar)
		currentVector=map(operator.itemgetter(3),file_evaluar)
		statusVector=map(int,statusVector)
		timeVector=map(int,timeVector)
		voltageVector=map(int,voltageVector)
		currentVector=map(int,currentVector)
		sizeVector=len(timeVector)
		
	#Main state machine
	#Main state machine
	if machineStatus == initState :
		if voltageVector[5] > umbralVoltHigh :
			machineStatus = initDischarge
			print "DISCHARGE,1.5"
		elif voltageVector[5] < umbralVoltLow :
			machineStatus = initCharge
			print "CHARGE,1.5"
		else :
			machineStatus = measureZ
			print "DISCHARGE,1.0"
	elif machineStatus == initDischarge :
		if voltageVector[sizeVector-5] < umbralVoltMin :
			machineStatus = rest1
			print "PAUSE"
		else :
			print "RUN"
	elif machineStatus == initCharge :
		if voltageVector[sizeVector-5] > umbralVoltMin :
			machineStatus = rest1
			print "PAUSE"
		else :
			print "RUN"
	elif machineStatus == rest1 :
		machineStatus = measureZ
		print "DISCHARGE,1.0"
	elif machineStatus == measureZ :
		v1 = voltageVector[sizeVector-15]
		v2 = voltageVector[sizeVector-5]
		i = currentVector[sizeVector-5]
		z = int((float(v2-v1)/float(i))*1000)
		storedMemory.set('GUI','line1','"Analysis Finished"')
		storedMemory.set('GUI','line2','"Health: ---    Internal Z: "'+str(z)+"mOhm")
		storedMemory.set('GUI','bgcolor','"244,123,183"')
		storedMemory.set('GUI','extra_info','"This is scriptTest2.py"')
		print "STOP,DCC,0,"+str(z)
	
	storedMemory.set('General','machineStatus',machineStatus)
	# Writing memory to 'stX.ini' file
	with open("data/st"+station+".ini", 'w') as configfile:
		storedMemory.write(configfile)
	
sys.exit()

	#	storedMemory.set('GUI','line1','"Analysis Finished - NTF"')
	#	storedMemory.set('GUI','line2','"Health: 68/100    Internal Z: 52mOhm"')
	#	storedMemory.set('GUI','bgcolor','"244,123,183"')
	#	storedMemory.set('GUI','extra_info','"Donec eu ultricies sem. Proin ut dictum lacus. Vestibulum cursus ipsum eget sem condimentum feugiat id ac arcu. Proin semper nulla sed metus mattis, et euismod mauris iaculis."')
	#	print "STOP,NTF,68,52"