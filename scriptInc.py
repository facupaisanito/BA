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
tTest1  =   20  #tiempo de descarga suave
tTest2  =   140  #tiempo de descarga fuerte
tTest3  =   400  #tiempo de recuperacion
tTest4  =   200 #tiempo de chequeo e incio de sig etapa
tTest5  =   20
tMargin =   3   #margen de tiempo por no ser 10s exactos
# voltageAverage = 3
# currentAverage = 5
# Z1 = 0
# Z2 = 0
tTestA  =   tTest1
tTestB  =   tTest1 + tTest2
tTestC  =   tTest1 + tTest2 + tTest3
tTestD  =   tTest1 + tTest2 + tTest3 + tTest4
#
def measure_z1() :
    if scriptSys.GENERAL['mode'] != 'Z_MEASURE' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'Z_MEASURE'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "DISCHARGE,1.8"
        return

    actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
    if  actual_time >= tTestD :
        # deja reposar y chequea q no caiga la tension
        final_report()
        # stress_test()
        # measure_z2()
        return

    if  actual_time >= (tTestC - tMargin)  and  actual_time < (tTestC + tMargin) :
        # print "DISCHARGE,1.0"  Descarga fuerte
        # scriptSys.import_data()
        # t = scriptSys.TIME_INIT + tTest1 + 2 #delay en el inicio de la descarga
        # var = scriptSys.get_data('VOLTAGE', range( t , t + voltageAverage))
        # V1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        # var = scriptSys.get_data('VOLTAGE', range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
        # V2 = sum(var) / float(len(var)) #promedio de las mediciones al final del test
        # var = scriptSys.get_data('CURRENT', range(scriptSys.TIME - currentAverage,scriptSys.TIME))
        # I1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        # Z2 = int((float(V2)/float(I1))*1000)
        # scriptSys.EVAL['int_z2'] = str(Z2)
        # scriptSys.EVAL['int_z'] =   str(Z2) #str(round(Z1,0))
        # chequear rectas
        print "PAUSE"
        return

    if  actual_time >= (tTestB - tMargin)  and  actual_time < (tTestB + tMargin) :
        # deja reposar y chequea q no caiga la tension
        # stress_test()
        print "DISCHARGE,1.0"
        # print "PAUSE"
        return

    if  actual_time >= (tTestA - tMargin)  and  actual_time < (tTestA + tMargin) :
        # print "DISCHARGE,0.2"  Descarga suave
        # scriptSys.import_data()
        # t = scriptSys.TIME_INIT + 2 #delay en el inicio de la descarga
        # var = scriptSys.get_data('VOLTAGE', range( t , t + voltageAverage))
        # V1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        # var = scriptSys.get_data('VOLTAGE', range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
        # V2 = sum(var) / float(len(var)) #promedio de las mediciones al final del test
        # var = scriptSys.get_data('CURRENT', range( scriptSys.TIME - currentAverage,scriptSys.TIME))
        # I1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        # Z1 = int((float(V2)/float(I1))*1000)
        # scriptSys.EVAL['int_z1'] =  str(Z1) #str(round(Z1,3))
        # chequear rectas
        print "PAUSE"
        return
    print "RUN"
    return
################################################################
##########                  measure_z2                ##########
################################################################
#Setup
tTest12  =   30  #tiempo de descarga suave
tTest22  =   60  #tiempo de descarga fuerte
tTest32  =   60  #tiempo de recuperacion
tTest42  =   20  #tiempo de chequeo e incio de sig etapa
tTest52  =   20
# tMargin =   5   #margen de tiempo por no ser 10s exactos
voltageAverage = 3
currentAverage = 5
Z1 = 0
Z2 = 0
tTestA2  =   tTest12
tTestB2  =   tTest12 + tTest22
tTestC2  =   tTest12 + tTest22 + tTest32
tTestD2  =   tTest12 + tTest22 + tTest32 + tTest42
#
def measure_z2() :
    if scriptSys.GENERAL['mode'] != 'Z_MEASURE2' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'Z_MEASURE2'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "DISCHARGE,1.0"
        return

    actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
    if  actual_time >= tTestD2 :
        # deja reposar y chequea q no caiga la tension
        # final_report()
        # stress_test()
        scriptSys.GENERAL['mode'] = 'CHARGE'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "CHARGE,4.2,1.2"
        # scriptTest.charge_state(1)
        return

    if  actual_time >= (tTestC2 - tMargin)  and  actual_time < (tTestC2 + tMargin) :
        # print "DISCHARGE,1.0"  Descarga fuerte
        scriptSys.import_data()
        t = scriptSys.TIME_INIT + tTestB2 + 2 #delay en el inicio de la descarga
        var = scriptSys.get_data('VOLTAGE', range( t - 5 , t - 5 + voltageAverage))
        V1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        var = scriptSys.get_data('VOLTAGE', range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
        V2 = sum(var) / float(len(var)) #promedio de las mediciones al final del test
        var = scriptSys.get_data('CURRENT', range(scriptSys.TIME - currentAverage,scriptSys.TIME))
        I1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        Z2 = int( ( (float(V2)-float(V1))/float(I1) ) *1000 )
        scriptSys.EVAL['int_z2'] = str(Z2)
        scriptSys.EVAL['int_z'] =   str(Z2) #str(round(Z1,0))
        # chequear rectas
        print "PAUSE"
        return

    if  actual_time >= (tTestB2 - tMargin)  and  actual_time < (tTestB2 + tMargin) :
        # deja reposar y chequea q no caiga la tension
        # stress_test()
        print "DISCHARGE,1.5"
        return

    if  actual_time >= (tTestA2 - tMargin)  and  actual_time < (tTestA2 + tMargin) :
        # print "DISCHARGE,0.2"  Descarga suave
        scriptSys.import_data()
        t = scriptSys.TIME_INIT + 2 #delay en el inicio de la descarga
        var = scriptSys.get_data('VOLTAGE', range( t - 5, t- 5 + voltageAverage))
        V1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        var = scriptSys.get_data('VOLTAGE', range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
        V2 = sum(var) / float(len(var)) #promedio de las mediciones al final del test
        var = scriptSys.get_data('CURRENT', range( scriptSys.TIME - currentAverage,scriptSys.TIME))
        I1 = sum(var) / float(len(var)) #promedio de las mediciones al principio
        Z1 = int( ( (float(V2)-float(V1))/float(I1) ) *1000 )

        scriptSys.EVAL['int_z1'] =  str(Z1) #str(round(Z1,3))
        # chequear rectas
        print "PAUSE"
        return
    print "RUN"
    return
################################################################
##########                  STRESS                    ##########
################################################################

#Setup
tStress =   600  #tiempo de descarga suave
tRest   =   120  #tiempo de descarga fuerte

#
def stress_test() :
    if scriptSys.GENERAL['mode'] != 'STRESS' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'STRESS'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "DISCHARGE,1.0"
        return

    actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)

    if  actual_time >= (tStress + tRest ) :# 5 ciclo terminado
        # print "PAUSE"
        final_report()
        return
    # if  actual_time >= (5*tStress + 4*tRest - tMargin) :
    #     print "PAUSE"
    #     return
    # if  actual_time >= (4*tStress + 4*tRest - tMargin)    and  actual_time < (5*tStress + 4*tRest + tMargin) :# 4 ciclo
    #     print "DISCHARGE,1.8"
    #     return
    # if  actual_time >= (4*tStress + 3*tRest - tMargin)    and  actual_time < (4*tStress + 4*tRest + tMargin) :
    #     print "PAUSE"
    #     return
    # if  actual_time >= (3*tStress + 3*tRest - tMargin)    and  actual_time < (4*tStress + 3*tRest + tMargin) :# 3 ciclo
    #     print "DISCHARGE,1.8"
    #     return
    # if  actual_time >= (3*tStress + 2*tRest - tMargin)    and  actual_time < (3*tStress + 3*tRest + tMargin) :
    #     print "PAUSE"
    #     return
    # if  actual_time >= (2*tStress + 2*tRest - tMargin)    and  actual_time < (3*tStress + 2*tRest + tMargin) :# 2 ciclo
    #     print "DISCHARGE,1.8"
    #     return
    # if  actual_time >= (2*tStress + tRest - tMargin)      and  actual_time < (2*tStress + 2*tRest + tMargin) :
    #     print "PAUSE"
    #     return
    # if  actual_time >= (tStress + tRest - tMargin)        and  actual_time < (2*tStress + tRest + tMargin) :   # 1 ciclo
    #     print "DISCHARGE,1.8"
    #     return
    if  actual_time >= (tStress - tMargin)                and  actual_time < (tStress + tMargin):
        print "PAUSE"
        return
    print "RUN"
    return
################################################################
##########                  EVALUATE                  ##########

################################################################

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
    scriptSys.copy_report()
    return
################################################################
##########                  ALREADY CHARGED           ##########
################################################################

#Setup
#
def already_charged() :
    if scriptSys.GENERAL['mode'] != 'END' : #si es llamado por primera vez
        scriptSys.GENERAL['mode'] = 'END'
        scriptSys.TIME_INIT = scriptSys.TIME
        print "STOP,NTF,100,0"

    scriptSys.GUI['line1'] = "Analysis Finished"
    scriptSys.GUI['line2'] = "Batery already CHARGED :"+ str(scriptSys.VOLTAGE) + 'V'
    scriptSys.GUI['bgcolor'] = '"120,244,183"'
    scriptSys.GUI['extra_info'] = " Z1="+scriptSys.EVAL['int_z1']+" Z2="+scriptSys.EVAL['int_z2']
    scriptSys.copy_report()
    return
