#-----------------------------------------------------------------------
# ScriptTest  for BA
# Version: 2
# Compatible with HW:
# Developed by Ignacio Cazzasa and company for CWG
#-----------------------------------------------------------------------

try:
    import sys,csv,operator,numbers,random,ConfigParser
except:
    print "import Error"
    sys.exit()

#==================================	
#SETUP
#Activate time parameters
activateSquareH = "1.0"		# corriente estado H square 
activateSquareL = "-1.0"	# corriente estado L square
activateSquareTime = "2"	# tiempo estado H y L square
activateTime = 20			# tiempo de estado activate
#OCV time parameters
ocvTime = 30
#Stress state parameters
stresCurrent = "1.8"		# Corriente de descarga durante proceso de stress
stresTime = 20				# Tiempo de stress
#Z measure parameters
zCurrent = "1.0"			# Corriente de descarga durante Medicion Z
zTime = 10					# Tiempo de descaga para Medicion Z
zTresholMax = 500#340 			# Maxima Z aceptada
zTresholMin = 20			# Minima Z aceptada
#Charge state parameters
chargeTime = 1200			# Maximo tiempo de carga
chargeVoltsMin = 3600		# Tension minima para efectuar la medicion Z
chargeVoltsFail = 3000		# Tension minima para realizar en analisis
chargeVoltsStop = 4000		# Tension para detener el proceso de caga
chargeCurrent = "1.0"		# Maxima corriente de carga
chargeVoltage = "4.2"		# Tension de carga
#Pause 1 time
pause1Time = 120			# Tiempo de reposo entre Carga y Medicion Z
#==================================	
#Machine Status
initState = "initState"
activeateState = "activeateState"
ocvState = "ocvState"
zState = "zState"
pause1State = "pause1State"
pause2State = "pause2State"
stresState = "stresState"
chargeState = "chargeState"
finishState = "finishState"
#==================================	
#Msg from the charger board
battConnected = 16
presenceConnected = 80
presenceDisconnected = 81


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#	MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def main() :
	arg_num=len(sys.argv)
	if(arg_num==2) :
		station=sys.argv[1]
				
		#Get the General stored memory information
		storedMemory = ConfigParser.SafeConfigParser()
		storedMemory.read("data/st"+station+".ini")
		entradas = storedMemory.getint('General','entradas')
		machineStatus = storedMemory.get('General','machineStatus')
		#Set the correct state machine status when executing for first time
		if entradas == 0 :
			#inicializacion de variables
			machineStatus = initState
			storedMemory.set('General','machineStatus',machineStatus)
		#Get the Eval stored memory information
		try :
			ocv = storedMemory.getint('Eval','ocv')	
			vz1 = storedMemory.getint('Eval','vz1')
			iz1 = storedMemory.getint('Eval','iz1')
			tz1 = storedMemory.getint('Eval','tz1')
			int_z = storedMemory.getint('Eval','int_z')
			tch = storedMemory.getint('Eval','tch')
			tst = storedMemory.getint('Eval','tst')
			tp1 = storedMemory.getint('Eval','tp1')
			aux1 = storedMemory.getint('Eval','aux1')
		except: 
			ocv = 0	#open circuit voltage 
			vz1 = 0	#voltage when measuring Z
			iz1 = 0	#current when measuring Z
			tz1 = 0 #time when start to measure Z
			int_z = 0	#internal z
			tch = 0 #time when start the charging process
			tst = 0 #time when start the stress process
			tp1 = 0 #time between charge and z measurment
			aux1 = 0 #variable auxiliar
			storedMemory.set('Eval','ocv',str(ocv))
			storedMemory.set('Eval','vz1',str(vz1))
			storedMemory.set('Eval','iz1',str(iz1))
			storedMemory.set('Eval','tz1',str(tz1))
			storedMemory.set('Eval','int_z',str(int_z))
			storedMemory.set('Eval','tch',str(tch))
			storedMemory.set('Eval','tst',str(tst))
			storedMemory.set('Eval','tp1',str(tp1))
			storedMemory.set('Eval','aux1',str(aux1))
		
		#Update entradas counter
		storedMemory.set('General','entradas',str(entradas+1))

		#Open the waveform
		csv_error=False
		try :
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
				msgVector=map(operator.itemgetter(7),file_evaluar)
				statusVector=map(int,statusVector)
				timeVector=map(int,timeVector)
				voltageVector=map(int,voltageVector)
				currentVector=map(int,currentVector)
				msgVector=map(int,msgVector)
				sizeVector=len(timeVector)
				currentTime=timeVector[sizeVector-1]
				currentVoltage=voltageVector[sizeVector-1]
				currentCurrent=currentVector[sizeVector-1]
		except:
			csv_error=True

		if ( csv_error == False ) :
			#Check if disconnection dettected
			if(presenceDisconnected in msgVector) :
				#fail por bateria desconectada
				storedMemory.set('GUI','line1','"DISCONNECTED"')
				storedMemory.set('GUI','line2','"Analysis Finished"')
				storedMemory.set('GUI','bgcolor','"240,250,120"')
				storedMemory.set('GUI','extra_info','"Battery disconnected 1"')
				machineStatus = finishState
				print "STOP,DC,STOP"
			#Main state machine
			if machineStatus == initState :
				aux1 = currentTime
				machineStatus = activeateState
				print str("SQUARE,"+activateSquareH+","+activateSquareL+","+activateSquareTime)
			elif machineStatus == activeateState :
				deltaTime = currentTime - aux1
				if ( deltaTime > activateTime ) :
					aux1 = currentTime
					machineStatus = ocvState
					print str("PAUSE")
				else :
					print "RUN"
			elif machineStatus == ocvState :		
				deltaTime = currentTime - aux1
				if ( deltaTime > activateTime ) :
					ocv = currentVoltage
					if( ocv >= chargeVoltsMin ) :
						tz1 = currentTime
						machineStatus = zState
						print str("DISCHARGE,"+zCurrent)
					elif ( ocv >= chargeVoltsFail ) :
						tch = currentTime
						machineStatus = chargeState
						print str("CHARGE,"+chargeVoltage+","+chargeCurrent)
					else :
						#fail por tension minima no alcanzada
						storedMemory.set('GUI','line1','"FAIL"')
						storedMemory.set('GUI','line2','"Analysis Finished"')
						storedMemory.set('GUI','bgcolor','"255,70,0"')
						storedMemory.set('GUI','extra_info','"Voltage fail 1"')
						machineStatus = finishState
						print "STOP,FAIL,FAIL"
				else :
					print "RUN"
			elif machineStatus == chargeState :
				deltaTime = currentTime - tch
				if ( deltaTime > chargeTime or currentVoltage > chargeVoltsStop ) :
					tp1 = currentTime
					machineStatus = pause1State
					print "PAUSE"
				else :
					if ( currentCurrent > 200 ) :
						print "RUN"
					else :
						tp1 = currentTime
						machineStatus = pause1State
						print "PAUSE"
			elif machineStatus == pause1State :	
				deltaTime = currentTime - tp1
				if ( deltaTime > pause1Time ) :
					tz1 = currentTime
					ocv = currentVoltage
					machineStatus = zState
					print str("DISCHARGE,"+zCurrent)
				else :
					print "RUN"
			elif machineStatus == zState :
				deltaTime = currentTime - tz1
				if ( deltaTime > zTime ) :
					vz1 = currentVoltage
					iz1 = abs(currentCurrent)
					int_z = int((float(float(ocv-vz1))/float(iz1))*1000)
					machineStatus = pause2State
					print "PAUSE"
				else :
					if ( currentCurrent < -10 ) :
						print "RUN"
					else :
						#fail por bateria desconectada
						storedMemory.set('GUI','line1','"FAIL"')
						storedMemory.set('GUI','line2','"Analysis Finished"')
						storedMemory.set('GUI','bgcolor','"255,70,0"')
						storedMemory.set('GUI','extra_info','"Voltage protection 1"')
						machineStatus = finishState
						print "STOP,FAIL,FAIL"
			elif machineStatus == pause2State :
				tst = currentTime
				machineStatus = stresState
				print str("DISCHARGE,"+stresCurrent)
			elif machineStatus == stresState :
				deltaTime = currentTime - tst
				if ( deltaTime > stresTime ) :
					if ( currentCurrent < -10 ) :
						if ( int_z < zTresholMax  and int_z > zTresholMin ) :
							#NTF
							storedMemory.set('GUI','line1','"NTF"')
							storedMemory.set('GUI','line2','"Analysis Finished"')
							storedMemory.set('GUI','bgcolor','"0,160,25"')
							storedMemory.set('GUI','extra_info','"A="'+str(int_z))
							machineStatus = finishState
							#print "STOP,NTF,NTF,"+str(int_z)
							print "STOP,NTF,NTF"
						else :
							#fail por Z
							storedMemory.set('GUI','line1','"FAIL"')
							storedMemory.set('GUI','line2','"Analysis Finished"')
							storedMemory.set('GUI','bgcolor','"255,70,0"')
							storedMemory.set('GUI','extra_info','"A="'+str(int_z))
							machineStatus = finishState
							#print "STOP,FAIL,FAIL,"+str(int_z)
							print "STOP,FAIL,FAIL"
					else :
						#fail por stress test
						storedMemory.set('GUI','line1','"FAIL"')
						storedMemory.set('GUI','line2','"Analysis Finished"')
						storedMemory.set('GUI','bgcolor','"255,70,0"')
						storedMemory.set('GUI','extra_info','"Stress test fail"')
						machineStatus = finishState
						print "STOP,FAIL,FAIL"
				else :
					if ( currentCurrent < -10 ) :
						print "RUN"
					else :
						#fail por bateria desconectada
						storedMemory.set('GUI','line1','"FAIL"')
						storedMemory.set('GUI','line2','"Analysis Finished"')
						storedMemory.set('GUI','bgcolor','"255,70,0"')
						storedMemory.set('GUI','extra_info','"Voltage protection 2"')
						machineStatus = finishState
						print "STOP,FAIL,FAIL"
					
			# Writing memory to 'stX.ini' file
			storedMemory.set('General','machineStatus',machineStatus)
			storedMemory.set('Eval','ocv',str(ocv))
			storedMemory.set('Eval','vz1',str(vz1))
			storedMemory.set('Eval','iz1',str(iz1))
			storedMemory.set('Eval','tz1',str(tz1))
			storedMemory.set('Eval','int_z',str(int_z))
			storedMemory.set('Eval','tch',str(tch))
			storedMemory.set('Eval','tst',str(tst))
			storedMemory.set('Eval','tp1',str(tp1))
			storedMemory.set('Eval','aux1',str(aux1))
			with open('data/st'+station+'.ini', 'w') as configfile:
				storedMemory.write(configfile)
		else :
			print "ERR2"
	else :
		print "ERR1"
	sys.exit()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#	EXECUTE MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
main()