#-----------------------------------------------------------------------
# ScriptTest  for BA
# Version: 1
# Compatible with HW:
# Developed by Ignacio Cazzasa and company for CWG
#-----------------------------------------------------------------------

try:
    import sys,os
except:
    print "import sys,os in scriptSys Not found!!"
    sys.exit()
try:
    sys.argv.append('--Param-scriptSys')
    sys.argv.append(sys.argv[1])
    import scriptSys
except:
    print "ERROR file scriptSys Not found!!"
    sys.exit()
try:
    sys.argv.append('--Param-scriptInc')
    sys.argv.append(sys.argv[1])
    import scriptInc
except:
    print "ERROR file scriptInc Not found!!"
    sys.exit()
for px in sys.argv:
    if px == '-d':
        scriptSys.DEBUG_MODE = True
        try:
            sys.argv.append('--Param-scriptDebug')
            sys.argv.append(sys.argv[1])
            import scriptDebug
        except:
            print "ERROR file scriptDebug Not found!!"
            sys.exit()

#Setup
umbralVoltTarget =  	3600

umbralVoltHigh =    	umbralVoltTarget * 1.02
umbralVoltLow =     	umbralVoltTarget * 0.98
umbralVolt =        	100
maxTimeInit =       	10          # 10 seg
maxTimeDischarge =  	30 * 60     # 30 min
minTimeDischarge =  	60
maxTimeCharge =     	1 * 60 * 60 # 1 hr
minTimeCharge =     	60
maxTimeCond =       	45          # 10 seg
tMargin =               3
iCharge1 =          	'1.8'
iCharge2 =          	'1.5'
iCharge3 =          	'1.3'
iCharge4 =          	'1.0'
vCharge1 =          	'4.1'
vCharge2 =          	'4.1'
vCharge3 =          	'4.1'
vCharge4 =          	'4.2'
iDischarge1 =       	'1.6'
iDischarge2 =       	'1.3'
iDischarge3 =       	'1.0'
iDischarge4 =       	'0.5'
################################################################
##########                  INIT                      ##########
################################################################
def init_state() :
    if int(scriptSys.TIME) >= maxTimeInit :
        if scriptSys.VOLTAGE <= umbralVoltLow:
            # charge_state(1)
            scriptInc.already_charged(1)
            sys.exit()
        if scriptSys.VOLTAGE > umbralVoltHigh:
            discharge_state(1)
            sys.exit()

        if scriptSys.VOLTAGE < umbralVoltHigh and \
            scriptSys.VOLTAGE > umbralVoltLow:
            scriptInc.already_charged(1)

            # zmeasure_state()
            sys.exit()
    print "RUN"
    scriptSys.ini_Update()
    sys.exit()
    return
################################################################
##########                  CHARGE                    ##########
################################################################
def charge_state(number) :
    if not scriptSys.GENERAL['mode'] == 'CHARGE' : #si es llamado por 1 vez
        scriptSys.GENERAL['mode'] = 'CHARGE'
        scriptSys.TIME_INIT = scriptSys.TIME
        if (umbralVoltTarget - scriptSys.VOLTAGE) < (0.05 * umbralVoltTarget):
            number = 4
        elif (umbralVoltTarget - scriptSys.VOLTAGE) < (0.1 * umbralVoltTarget):
            number = 3
        elif (umbralVoltTarget - scriptSys.VOLTAGE) < (0.2 * umbralVoltTarget):
            number = 2
        else:
            number = 1
        if number == 4 : print "CHARGE,"+ vCharge4 +","+ iCharge4
        if number == 3 : print "CHARGE,"+ vCharge3 +","+ iCharge3
        if number == 2 : print "CHARGE,"+ vCharge2 +","+ iCharge2
        if number == 1 : print "CHARGE,"+ vCharge1 +","+ iCharge1
        scriptSys.ini_Update()
        return

    if  scriptSys.VOLTAGE > (umbralVoltTarget + umbralVolt) and \
        (scriptSys.TIME - scriptSys.TIME_INIT) >= minTimeCharge:
        cond_state()
        sys.exit()

    if (int(scriptSys.TIME) - int(scriptSys.TIME_INIT)) >= maxTimeCharge :
        scriptSys.GENERAL['mode']= "STOP"
        print "STOP"
        scriptSys.GUI['line1'] = "Analysis Stopped"
        scriptSys.GUI['line2'] = "Max time of CHARGE reached"
        scriptSys.GUI['bgcolor'] = '"244,0,0"'
        scriptSys.GUI['extra_info'] = "This is scriptTest.py"
        scriptSys.ini_Update()
        sys.exit()
    print "RUN"
    scriptSys.ini_Update()
    sys.exit()  #continua esperando
    return
################################################################
##########                  DISCHARGE                 ##########
################################################################
def discharge_state(number) :
    if not scriptSys.GENERAL['mode'] == 'DISCHARGE' : #si es llamado por 1 vez
        scriptSys.GENERAL['mode'] = 'DISCHARGE'
        scriptSys.TIME_INIT = scriptSys.TIME
        if (scriptSys.VOLTAGE - umbralVoltTarget)  >  (0.2 * umbralVoltTarget):
            number = 1
        elif (scriptSys.VOLTAGE - umbralVoltTarget) > (0.05 * umbralVoltTarget):
            number = 2
        elif (scriptSys.VOLTAGE - umbralVoltTarget) > (0.01 * umbralVoltTarget):
            number = 3
        else:
            number = 4
        if number == 1 : print "DISCHARGE,"+ iDischarge1
        if number == 2 : print "DISCHARGE,"+ iDischarge2
        if number == 3 : print "DISCHARGE,"+ iDischarge3
        if number == 4 : print "DISCHARGE,"+ iDischarge4
        scriptSys.ini_Update()
        sys.exit()
        return

    if scriptSys.VOLTAGE < (umbralVoltTarget - umbralVolt) \
        and (scriptSys.TIME - scriptSys.TIME_INIT) >= minTimeDischarge:
        cond_state()
        sys.exit()

    if (int(scriptSys.TIME) - int(scriptSys.TIME_INIT)) >= maxTimeDischarge :
        scriptSys.TIME_INIT = scriptSys.TIME
        scriptSys.GENERAL['mode']= "STOP"
        print "STOP"
        scriptSys.GUI['line1'] = "Analysis Stopped"
        scriptSys.GUI['line2'] = "Max time of DISCHARGE reached"
        scriptSys.GUI['bgcolor'] = '"244,0,0"'
        scriptSys.GUI['extra_info'] = "This is scriptTest.py"
        scriptSys.ini_Update()
        sys.exit()
    print "RUN"
    scriptSys.ini_Update()
    sys.exit()  #continua esperando
    return
################################################################
##########                  CONDITIONING               #########
################################################################
def cond_state():
    if not scriptSys.GENERAL['mode'] == 'CONDITIONING' : #es llamado por 1 vez
        scriptSys.GENERAL['mode'] = 'CONDITIONING'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "PAUSE"
        scriptSys.ini_Update()
        sys.exit()

    if  ((scriptSys.TIME) - (scriptSys.TIME_INIT)) >= (maxTimeCond - tMargin):
        # if scriptSys.VOLTAGE < umbralVoltLow:
        #     charge_state(2)
        #     scriptSys.ini_Update()
        #     sys.exit()
        #     return


        if scriptSys.VOLTAGE > umbralVoltHigh:
            discharge_state(2)
            scriptSys.ini_Update()
            sys.exit()
        # if scriptSys.VOLTAGE < umbralVoltHigh and \
        #     scriptSys.VOLTAGE > umbralVoltLow:
        #     scriptInc.measure_z1()
        #     scriptSys.ini_Update()
        #     sys.exit()
        scriptInc.already_charged(2)
    print "RUN"
    scriptSys.ini_Update()
    sys.exit()  #continua esperando
    return
################################################################
##########                  Z_MEASURE                 ##########
################################################################
def zmeasure_state() :
    scriptInc.measure_z1()

    scriptSys.ini_Update()
    sys.exit()
    return
################################################################
##########                  Z_MEASURE                 ##########
################################################################
def zmeasure2_state() :
    scriptInc.measure_z2()

    scriptSys.ini_Update()
    sys.exit()
    return
################################################################
##########                  STRESS                     ##########
################################################################
def stress_state():
    scriptInc.stress_test()

    scriptSys.ini_Update()
    sys.exit()
    return
################################################################
##########                  PAUSE                     ##########
################################################################
def pause_state():
    print "RUN"
    scriptSys.ini_Update()
    sys.exit()  #continua esperando
    return
################################################################
##########                  END                       ##########
################################################################
def end_state():
    scriptSys.GENERAL['mode']= "STOP"
    scriptSys.TIME_INIT = scriptSys.TIME
    print "STOP"
    # scriptSys.copy_report()
    scriptSys.ini_Update()
    sys.exit()
    return


# print "SET,4.2,1.0,1.2"
# print "SET"
# print "STOP"
# print "STOP,NTF"
# print "STOP,FAIL,150,68"
# print "STOP,DCC,0,"+str(z)
# print "CHARGE"
# print "CHARGE,4.2,0.8"
# print "DISCHARGE"
# print "DISCHARGE,1.2"
# print "PAUSE"
# print "FIND"
# print "DISABLE"
# print "ENABLE"

################################################################
##########                  MAIN                      ##########
################################################################
if  scriptSys.GENERAL['mode'] == "INIT":
    init_state()
if scriptSys.GENERAL['mode'] == "CHARGE":
    charge_state(1)
if scriptSys.GENERAL['mode'] == "DISCHARGE":
    discharge_state(1)
if scriptSys.GENERAL['mode'] == "CONDITIONING":
    cond_state()
if scriptSys.GENERAL['mode'] == "Z_MEASURE":
    zmeasure_state()
if scriptSys.GENERAL['mode'] == "Z_MEASURE2":
    zmeasure2_state()
if scriptSys.GENERAL['mode'] == "STRESS":
    stress_state()
if scriptSys.GENERAL['mode'] == "PAUSE":
    pause_state()
if scriptSys.GENERAL['mode'] == "END":
    end_state()
    sys.exit()
