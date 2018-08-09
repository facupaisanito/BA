#-----------------------------------------------------------------------
# ScriptTest  for BA
# Version: 12
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
    print "ERROR file scriptSys Not found in scriptTest!!"
    sys.exit()
try:
    sys.argv.append('--Param-scriptInc')
    sys.argv.append(sys.argv[1])
    import scriptInc
except:
    print "ERROR file scriptInc Not found in scriptTest!!"
    sys.exit()
for px in sys.argv:
    if px == '-d':
        scriptSys.DEBUG_MODE = True
        try:
            sys.argv.append('--Param-scriptDebug')
            sys.argv.append(sys.argv[1])
            import scriptDebug
        except:
            print "ERROR file scriptDebug Not found in scriptTest!!"
            sys.exit()

################################################################
##########                  SETUP                     ##########
################################################################
umbralVoltTarget =  	4100
umbralCurrentTarget =   400
umbralVoltHigh =    	umbralVoltTarget
umbralVoltLow =     	3200
umbralVolt =        	umbralVoltTarget * 0.03
maxTimeInit =       	40          # 10 seg
maxTimeDischarge =  	30 * 60     # 30 min
minTimeDischarge =  	60
maxTimeCharge =     	4 * 60 * 60 # 1 hr
minTimeCharge =     	2 * 60
maxTimeCond =       	60          # 10 seg
tMargin =               3
iCharge1 =          	'0.5'
iCharge2 =          	'1.8'
iCharge3 =          	'1.3'
iCharge4 =          	'1.0'
vCharge1 =          	'4.1'
vCharge2 =          	'4.2'
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
    try:
        if int(scriptSys.TIME) >= maxTimeInit :
            charge_state(1)
            return
            # if scriptSys.VOLTAGE <= umbralVoltLow:
            #     charge_state(1)
            #     return
            # if scriptSys.VOLTAGE > umbralVoltLow:
            #     stress_state()
            #     return
            #
            # if scriptSys.VOLTAGE < umbralVoltHigh and \
            #     scriptSys.VOLTAGE > umbralVoltLow:
            #     stress_state()
            #     return
        print "RUN"
        return
    except:
        scriptSys.error_report("init_state()")
################################################################
##########                  CHARGE                    ##########
################################################################
def charge_state(number) :
    try:
        if not scriptSys.GENERAL['mode'] == 'CHARGE' : #si es llamado por 1 vez
            scriptSys.GENERAL['mode'] = 'CHARGE'
            scriptSys.TIME_INIT = scriptSys.TIME
            # if (umbralVoltTarget - scriptSys.VOLTAGE) <(0.1*umbralVoltTarget):
            #     number = 4
            # elif (umbralVoltTarget -scriptSys.VOLTAGE)<(0.2*umbralVoltTarget):
            #     number = 3
            # elif (umbralVoltTarget -scriptSys.VOLTAGE)<(0.4*umbralVoltTarget):
            #     number = 2
            # else:
            #     number = 1
            # if number == 4 : print "CHARGE,"+ vCharge4 +","+ iCharge4
            # if number == 3 : print "CHARGE,"+ vCharge3 +","+ iCharge3
            # if number == 1 :
            print "CHARGE,"+ vCharge1 +","+ iCharge1
            return

        if  scriptSys.CURRENT <= (umbralCurrentTarget) and \
            (scriptSys.TIME - scriptSys.TIME_INIT) >= minTimeCharge:
            cond_state()
            return

        if (int(scriptSys.TIME) - int(scriptSys.TIME_INIT)) >= maxTimeCharge :
            scriptInc.final_report("maxTimeCharge")
            return
        # print "RUN"
        print "CHARGE,"+ vCharge2 +","+ iCharge2
        return
    except:
        scriptSys.error_report("charge_state()")
################################################################
##########                  DISCHARGE                 ##########
################################################################
def discharge_state(number) :
    try:
        if not scriptSys.GENERAL['mode'] == 'DISCHARGE' : #si es llamado por 1
            scriptSys.GENERAL['mode'] = 'DISCHARGE'
            scriptSys.TIME_INIT = scriptSys.TIME
            if number == 1 : print "DISCHARGE,"+ iDischarge1
            if number == 2 : print "DISCHARGE,"+ iDischarge2
            if number == 3 : print "DISCHARGE,"+ iDischarge3
            return

        if scriptSys.VOLTAGE < (umbralVoltTarget - umbralVolt) \
            and (scriptSys.TIME - scriptSys.TIME_INIT) >= minTimeDischarge:
            cond_state()
            return

        if (int(scriptSys.TIME) - int(scriptSys.TIME_INIT)) >= maxTimeDischarge:
            scriptInc.final_report("maxTimeDischarge")
            return
        print "RUN"
        return
    except:
        scriptSys.error_report("discharge_state()")
################################################################
##########                  CONDITIONING               #########
################################################################
def cond_state():
    try:
        if not scriptSys.GENERAL['mode'] == 'CONDITIONING' : #es llamado por 1
            scriptSys.GENERAL['mode'] = 'CONDITIONING'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "PAUSE"
            return

        if  ((scriptSys.TIME) - (scriptSys.TIME_INIT)) >= (maxTimeCond-tMargin):
            stress_state()
            return
            # if scriptSys.VOLTAGE < umbralVoltLow:
            #     charge_state(2)
            #     scriptSys.ini_Update()
            #     sys.exit()
            #     return
            #
            # scriptInc.already_charged()

            # if scriptSys.VOLTAGE > umbralVoltHigh:
            #     discharge_state(2)
            #     scriptSys.ini_Update()
            #     sys.exit()
            # if scriptSys.VOLTAGE < umbralVoltHigh and \
            #     scriptSys.VOLTAGE > umbralVoltLow:
            #     scriptInc.measure_z1()
            #     scriptSys.ini_Update()
            #     sys.exit()
        print "RUN"
        return
    except:
        scriptSys.error_report("cond_state()")
################################################################
##########                  Z_MEASURE                 ##########
################################################################
def zmeasure_state() :
    try:
        scriptInc.measure_z1()
        return
    except:
        scriptSys.error_report("zmeasure_state()")
################################################################
##########                  Z_MEASURE                 ##########
################################################################
def zmeasure2_state() :
    try:
        scriptInc.measure_z2()
        return
    except:
        scriptSys.error_report("zmeasure2_state()")
################################################################
##########                  STRESS                     ##########
################################################################
def stress_state():
    try:
        scriptInc.stress_test()
        return
    except:
        scriptSys.error_report("stress_state()")
################################################################
##########                  PAUSE                     ##########
################################################################
def pause_state():
    try:
        print "RUN"
        return
    except:
        scriptSys.error_report("pause_state()")
################################################################
##########                  END                       ##########
################################################################
def end_state():
    try:
        scriptSys.GENERAL['mode']= "STOP"
        scriptSys.TIME_INIT = scriptSys.TIME
        print "STOP"
        # scriptSys.copy_report()
        return
    except:
        scriptSys.error_report("end_state()")


# print "SET,4.2,1.0,1.2"
# print "SET"
# print "STOP"
# print "STOP,NTF"
# print "`STOP,FAIL,150,68"`
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
################################################################
##########                  MAIN                      ##########
################################################################
################################################################
if  scriptSys.GENERAL['mode'] == "INIT":
    init_state()
elif scriptSys.GENERAL['mode'] == "CHARGE":
    charge_state(1)
elif scriptSys.GENERAL['mode'] == "DISCHARGE":
    discharge_state(1)
elif scriptSys.GENERAL['mode'] == "CONDITIONING":
    cond_state()
elif scriptSys.GENERAL['mode'] == "Z_MEASURE":
    zmeasure_state()
elif scriptSys.GENERAL['mode'] == "Z_MEASURE2":
    zmeasure2_state()
elif scriptSys.GENERAL['mode'] == "STRESS":
    stress_state()
elif scriptSys.GENERAL['mode'] == "PAUSE":
    pause_state()
elif scriptSys.GENERAL['mode'] == "END":
    end_state()
scriptSys.ini_Update()
sys.exit()
