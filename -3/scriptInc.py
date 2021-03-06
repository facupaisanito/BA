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
tTest1  =   10  #tiempo de descarga suave
tTest2  =   20  #tiempo de descarga fuerte
tTest3  =   20  #tiempo de recuperacion
tTest4  =   20  #tiempo de chequeo e incio de sig etapa
tTest5  =   20
voltageAverage = 3
currentAverage = 10
Z1 = 0
Z2 = 0
#
def measure_z1() :
    if scriptSys.GENERAL['mode'] != 'Z_MEASURE' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'Z_MEASURE'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "DISCHARGE,0.2"

    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (tTest3 + tTest2 + tTest1) :
        # deja reposar y chequea q no caiga la tension
        scriptSys.import_data() #levanto todo el archivo solo cuando lo necesito
        t = scriptSys.TIME_INIT + tTest1 + tTest2
        var = scriptSys.get_data('VOLTAGE', range( t , t + voltageAverage))
        # chequear rectas
        stress_test()
    elif  (scriptSys.TIME - scriptSys.TIME_INIT) >= (tTest2 + tTest1) :
        # print "DISCHARGE,1.0"   Descarga fuerte
        scriptSys.import_data()
        t = scriptSys.TIME_INIT + tTest1
        var = scriptSys.get_data('VOLTAGE', range( t , t + voltageAverage))
        V1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        var = scriptSys.get_data('VOLTAGE', range( t + tTest2, t+ tTest2 + voltageAverage))
        V2 = sum(var) / float(len(var)) #promedio de las mediciones al final del test
        var = scriptSys.get_data('CURRENT', range( t, t + currentAverage))
        I1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        Z2 = int((float(V2-V1)/float(I1))*1000)
        scriptSys.EVAL['int_z2'] = Z2
        # chequear rectas
    elif  (scriptSys.TIME - scriptSys.TIME_INIT) >= tTest1 :
        # print "DISCHARGE,0.2"  Descarga suave
        scriptSys.import_data()
        t = scriptSys.TIME_INIT
        var = scriptSys.get_data('VOLTAGE', range( t , t + voltageAverage))
        V1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        var = scriptSys.get_data('VOLTAGE', range( t + tTest1, t+ tTest1 + voltageAverage))
        V2 = sum(var) / float(len(var)) #promedio de las mediciones al final del test
        var = scriptSys.get_data('CURRENT', range( t, t + currentAverage))
        I1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        Z1 = int((float(V2-V1)/float(I1))*1000)
        scriptSys.EVAL['int_z1'] = Z1
        # chequear rectas
        print "DISCHARGE,1.0"
    return
################################################################
##########                  STRESS                    ##########
################################################################

#Setup
tStress =   10  #tiempo de descarga suave
tRest   =   10  #tiempo de descarga fuerte
voltageAverage = 3
currentAverage = 10
#
def stress_test() :
    if scriptSys.GENERAL['mode'] != 'STRESS' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'STRESS'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "DISCHARGE,1.8"

    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (5*tStress + 5*tRest) :# 5 ciclo terminado
        print "PAUSE"
        final_report()
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (5*tStress + 4*tRest) :
        print "PAUSE"
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (4*tStress + 4*tRest) :# 4 ciclo
        print "DISCHARGE,1.8"
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (4*tStress + 3*tRest) :
        print "PAUSE"
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (3*tStress + 3*tRest) :# 3 ciclo
        print "DISCHARGE,1.8"
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (3*tStress + 2*tRest) :
        print "PAUSE"
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (2*tStress + 2*tRest) :# 2 ciclo
        print "DISCHARGE,1.8"
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (2*tStress + tRest) :
        print "PAUSE"
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (tStress + tRest) :   # 1 ciclo
        print "DISCHARGE,1.8"
    if  (scriptSys.TIME - scriptSys.TIME_INIT) >= (tStress) :
        print "PAUSE"
    return
################################################################
##########                  FINAL REPORT              ##########
################################################################

#Setup
#
def final_report() :
    if scriptSys.GENERAL['mode'] != 'STRESS' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'STRESS'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "STOP"

    scriptSys.EVAL['line1'] = "Analysis Finished"
    scriptSys.EVAL['line2'] = "Health: ---    Internal Z: " + str(1) + "mOhm"
    scriptSys.EVAL['bgcolor'] = "244,123,183"
    scriptSys.EVAL['extra_info'] = "This is scriptTest2.py"

    return
