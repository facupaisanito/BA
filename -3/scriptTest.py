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
umbralVoltHigh =    3800
umbralVoltMin =     3600
umbralVoltLow =     3200
maxTimeInit =       20          # 20 seg
maxTimeDischarge =  30 * 60     # 30 min
maxTimeCharge =     1 * 60 * 60 # 1 hr
maxTimeCondit =     20          # 20 seg

if scriptSys.DEBUG_MODE : scriptInc.get_line('VOLTAGE', range(40,60) )
scriptSys.import_data()
################################################################
##########                  INIT                      ##########
################################################################
def init_state() :
    if int(scriptSys.TIME) > maxTimeInit :
        if scriptSys.VOLTAGE < umbralVoltLow:
            scriptSys.TIME_INIT = scriptSys.TIME
            scriptSys.GENERAL['mode'] = "CHARGE"
            print "CHARGE,4.5,1.0"
            scriptSys.ini_Update()
            sys.exit()
        if scriptSys.VOLTAGE > umbralVoltHigh:
            scriptSys.TIME_INIT = scriptSys.TIME
            scriptSys.GENERAL['mode'] = "DISCHARGE"
            print "DISCHARGE,1.5"
            scriptSys.ini_Update()
            sys.exit()

        if scriptSys.VOLTAGE < umbralVoltHigh & scriptSys.VOLTAGE > umbralVoltLow:
            scriptSys.TIME_INIT = scriptSys.TIME
            scriptSys.GENERAL['mode']= "CONDITIONING"
            print "PAUSE"
    print "RUN"
    scriptSys.ini_Update()
    sys.exit()
    return
################################################################
##########                  CHARGE                    ##########
################################################################
def charge_state() :
    if scriptSys.VOLTAGE < umbralVoltHigh & scriptSys.VOLTAGE > umbralVoltLow:
        scriptSys.TIME_INIT = scriptSys.TIME
        scriptSys.GENERAL['mode']= "CONDITIONING"
        print "PAUSE"
        scriptSys.ini_Update()
        sys.exit()

    if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeCharge :
        scriptSys.GENERAL['mode']= "STOP"
        print "STOP"
        scriptSys.EVAL['line1'] = "Analysis Stopped"
        scriptSys.EVAL['line2'] = "Max time of CHARGE reached"
        scriptSys.EVAL['bgcolor'] = "244,0,0"
        scriptSys.EVAL['extra_info'] = "This is scriptTest.py"
        scriptSys.ini_Update()
        sys.exit()
    print "RUN"
    scriptSys.ini_Update()
    sys.exit()  #continua esperando
    return
################################################################
##########                  DISCHARGE                 ##########
################################################################
def discharge_state() :
    if scriptSys.VOLTAGE < umbralVoltHigh & scriptSys.VOLTAGE > umbralVoltLow:
        scriptSys.TIME_INIT = scriptSys.TIME
        scriptSys.GENERAL['mode']= "CONDITIONING"
        print "PAUSE"
        scriptSys.ini_Update()
        sys.exit()

    if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeDischarge :
        scriptSys.TIME_INIT = scriptSys.TIME
        scriptSys.GENERAL['mode']= "STOP"
        print "STOP"
        scriptSys.EVAL['line1'] = "Analysis Stopped"
        scriptSys.EVAL['line2'] = "Max time of DISCHARGE reached"
        scriptSys.EVAL['bgcolor'] = "244,0,0"
        scriptSys.EVAL['extra_info'] = "This is scriptTest.py"
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
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeCond:
        if scriptSys.VOLTAGE < umbralVoltLow:
            scriptSys.GENERAL['mode'] = "CHARGE"
            scriptSys.TIME_INIT = scriptSys.TIME
            print "CHARGE,4.5,1.0"
            scriptSys.ini_Update()
            sys.exit()
        if scriptSys.VOLTAGE > umbralVoltHigh:
            scriptSys.GENERAL['mode'] = "DISCHARGE"
            scriptSys.TIME_INIT = scriptSys.TIME
            print "DISCHARGE,1.5"
            scriptSys.ini_Update()
            sys.exit()
        if scriptSys.VOLTAGE < umbralVoltHigh & scriptSys.VOLTAGE > umbralVoltLow:
            scriptInc.measure_z1()
            scriptSys.ini_Update()
            sys.exit()
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
##########                  STRESS                     ##########
################################################################
def stress_state():
    scriptInc.stress()
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
    charge_state()
if scriptSys.GENERAL['mode'] == "DISCHARGE":
    discharge_state()
if scriptSys.GENERAL['mode'] == "CONDITIONING":
    cond_state()
if scriptSys.GENERAL['mode'] == "Z_MEASURE":
    zmeasure_state()
if scriptSys.GENERAL['mode'] == "STRESS":
    stress_state()
if scriptSys.GENERAL['mode'] == "PAUSE":
    pause_state()
if scriptSys.GENERAL['mode'] == "END":
    end_state()
    sys.exit()
