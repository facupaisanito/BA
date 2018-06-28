#-----------------------------------------------------------------------
# ScriptInc  for BA
# Version: 1
# Compatible with HW:
# Developed by Ignacio Cazzasa and company for CWG
#-----------------------------------------------------------------------
#
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
for px in sys.argv:
    if px == '--Param-scriptInc':
        idx = sys.argv.index(px)
        sys.argv.pop(idx) # remove option
        STATION_N = sys.argv[idx]
        sys.argv.pop(idx) # remove value

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
################################################################
##########                  line1                     ##########
################################################################
def get_line(dType, tLapse):
        n = len(tLapse)
        if len(tLapse)%2 == 1:
            tLapse.pop()
            n = len(tLapse)
        var = scriptSys.get_data(dType, tLapse)
        VAR = sum(var) / float(len(var)) #promedio
        m = []
        m_aux = []
        for x in range(0 , n , 2):
            m_aux.append((var[x]+var[x+1])/2)
        for x in range((n/2)-1):
            m.append((m_aux[x+1]-m_aux[x])/2)
        M = sum(m) / float(len(m)) #promedio
        VAR1 = VAR + M *(n/2)
        if scriptSys.DEBUG_MODE : scriptDebug.plot_line(dType,M,VAR1,tLapse[-1])
        scriptSys.GENERAL['line_m'] = str(M)
        scriptSys.GENERAL['line_m'] = str(VAR1)
        return
################################################################
##########                  measure_z1                ##########
################################################################
#Setup
tTest1  =   8  #tiempo de descarga suave
tTest2  =   28  #tiempo de descarga fuerte
tTest3  =   8  #tiempo de recuperacion
tTest4  =   20  #tiempo de chequeo e incio de sig etapa
tTest5  =   20
tMargin =   5   #margen de tiempo por no ser 10s exactos
voltageAverage = 3
currentAverage = 5
Z1 = 0
Z2 = 0
tTestA  =   tTest1
tTestB  =   tTest1 + tTest2
tTestC  =   tTest1 + tTest2 + tTest3
#
def measure_z1() :
    if scriptSys.GENERAL['mode'] != 'Z_MEASURE' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'Z_MEASURE'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "DISCHARGE,0.2"
        return

    actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
    if  actual_time >= tTestC :
        # deja reposar y chequea q no caiga la tension
        final_report()
        # stress_test()
        return

    if  actual_time >= tTestB  and  actual_time < (tTestB + tMargin) :
        # print "DISCHARGE,1.0"  Descarga fuerte
        scriptSys.import_data()
        t = scriptSys.TIME_INIT + tTest1 + 2 #delay en el inicio de la descarga
        var = scriptSys.get_data('VOLTAGE', range( t , t + voltageAverage))
        V1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        var = scriptSys.get_data('VOLTAGE', range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
        V2 = sum(var) / float(len(var)) #promedio de las mediciones al final del test
        var = scriptSys.get_data('CURRENT', range(scriptSys.TIME - currentAverage,scriptSys.TIME))
        I1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        Z2 = int((float(V2-V1)/float(I1))*1000)
        scriptSys.EVAL['int_z2'] = str(Z2)
        scriptSys.EVAL['int_z'] =   str(Z2) #str(round(Z1,0))
        # chequear rectas
        print "PAUSE"
        return

    if  actual_time >= tTestA  and  actual_time < (tTestA + tMargin) :
        # print "DISCHARGE,0.2"  Descarga suave
        scriptSys.import_data()
        t = scriptSys.TIME_INIT + 2 #delay en el inicio de la descarga
        var = scriptSys.get_data('VOLTAGE', range( t , t + voltageAverage))
        V1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        var = scriptSys.get_data('VOLTAGE', range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
        V2 = sum(var) / float(len(var)) #promedio de las mediciones al final del test
        var = scriptSys.get_data('CURRENT', range( scriptSys.TIME - currentAverage,scriptSys.TIME))
        I1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        Z1 = int((float(V2-V1)/float(I1))*1000)
        scriptSys.EVAL['int_z1'] =  str(Z1) #str(round(Z1,3))
        # chequear rectas
        if scriptSys.DEBUG_MODE: print scriptSy
        print "DISCHARGE,1.0"
        return
    print "RUN"
    return
################################################################
##########                  STRESS                    ##########
################################################################

#Setup
tStress =   9  #tiempo de descarga suave
tRest   =   9  #tiempo de descarga fuerte

#
def stress_test() :
    if scriptSys.GENERAL['mode'] != 'STRESS' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'STRESS'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "DISCHARGE,1.8"
    actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)

    if  actual_time >= (5*tStress + 5*tRest) :# 5 ciclo terminado
        # print "PAUSE"
        final_report()
        return
    if  actual_time >= (5*tStress + 4*tRest) :
        print "PAUSE"
    if  actual_time >= (4*tStress + 4*tRest)    and  actual_time < (5*tStress + 4*tRest) :# 4 ciclo
        print "DISCHARGE,1.8"
    if  actual_time >= (4*tStress + 3*tRest)    and  actual_time < (4*tStress + 4*tRest) :
        print "PAUSE"
    if  actual_time >= (3*tStress + 3*tRest)    and  actual_time < (4*tStress + 3*tRest) :# 3 ciclo
        print "DISCHARGE,1.8"
    if  actual_time >= (3*tStress + 2*tRest)    and  actual_time < (3*tStress + 3*tRest) :
        print "PAUSE"
    if  actual_time >= (2*tStress + 2*tRest)    and  actual_time < (3*tStress + 2*tRest) :# 2 ciclo
        print "DISCHARGE,1.8"
    if  actual_time >= (2*tStress + tRest)      and  actual_time < (2*tStress + 2*tRest) :
        print "PAUSE"
    if  actual_time >= (tStress + tRest)        and  actual_time < (2*tStress + tRest) :   # 1 ciclo
        print "DISCHARGE,1.8"
    if  actual_time >= (tStress)                and  actual_time < (tStress + tRest):
        print "PAUSE"
    return

################################################################
##########                  FINAL REPORT              ##########
################################################################

#Setup
#
def final_report() :
    if scriptSys.GENERAL['mode'] != 'END' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'END'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "STOP,NTF,75,"+ scriptSys.EVAL['int_z']

    scriptSys.GUI['line1'] = "Analysis Finished"
    scriptSys.GUI['line2'] = "Health: ---    Internal Z: " + str(scriptSys.EVAL['int_z']) + "mOhm"
    scriptSys.GUI['bgcolor'] = '"120,244,183"'
    scriptSys.GUI['extra_info'] = " Z1="+scriptSys.EVAL['int_z1']+" Z2="+scriptSys.EVAL['int_z2']
    scriptSys.ini_Update()
    scriptSys.copy_report()
    sys.exit()
    return
