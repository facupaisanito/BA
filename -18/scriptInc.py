#-----------------------------------------------------------------------
# ScriptInc  for BA
# Version: 1
# Compatible with HW:
# Developed by Ignacio Cazzasa and company for CWG
#-----------------------------------------------------------------------
#
################################################################
################################################################
##########                  SETUP                     ##########
################################################################
################################################################
ACTIVATION_TEST = False     #SQUARE AND CHARGE OF ACTIVATION
STRESS_TIME = 270           #EN SEG
STRESS_CURRENT = '1.0'      #STRING CON X.XA COMO POR COMANDO
Z_BOUNDARY = 70
################################################################
################################################################


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
    for px in sys.argv:
        if px == '--Param-scriptInc':
            idx = sys.argv.index(px)
            sys.argv.pop(idx) # remove option
            STATION_N = sys.argv[idx]
            sys.argv.pop(idx) # remove value
except:
    print "ERROR Param-scriptInc en scriptInc !!"
    sys.exit()
try:
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
except:
    print "ERROR Param-scriptDebug en scriptInc !!"
    sys.exit()
################################################################
##########                  line1                     ##########
################################################################
def get_line(dType, tLapse):
    try:
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
        scriptSys.AUX['line_m'] = str(M)
        scriptSys.AUX['line_m'] = str(VAR1)
        return
    except Exception as e:
        scriptSys.error_report(e,"get_line()")
################################################################
##########                  measure_z1                ##########
################################################################
#Setup
tTest1  =   30  #tiempo de descarga suave
tTest2  =   30  #tiempo de descarga fuerte
tTest3  =   60 #tiempo de recuperacion
tTest4  =   30 #tiempo de chequeo e incio de sig etapa
tTest5  =   20
tMargin =   5   #margen de tiempo por no ser 10s exactos
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
    try:
        if not ACTIVATION_TEST: stress_test()
        if scriptSys.GENERAL['mode'] != 'Z_MEASURE' : #si es 1 llamado
            scriptSys.GENERAL['mode'] = 'Z_MEASURE'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "SQUARE,1.0,-1.0,2"
            return

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        if  actual_time >= tTestD :
            stress_test()
            return
        if  actual_time >= (tTestC- tMargin)and actual_time <(tTestC + tMargin):
            print "PAUSE"
            return
        if  actual_time >=(tTestB - tMargin)and actual_time <(tTestB + tMargin):
            print "CHARGE,4.2,1.8"
            return
        if  actual_time >=(tTestA - tMargin)and actual_time <(tTestA + tMargin):
            print "PAUSE"
            return
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"measure_z1()")
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
    try:
        if scriptSys.GENERAL['mode'] != 'Z_MEASURE2' : #si es llamado por 1
            scriptSys.GENERAL['mode'] = 'Z_MEASURE2'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "DISCHARGE,1.0"
            return

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        if  actual_time >= tTestD2 :
            # deja reposar y chequea q no caiga la tension
            # final_report(0,0)
            # stress_test()
            scriptSys.GENERAL['mode'] = 'CHARGE'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "CHARGE,4.2,1.2"
            # scriptTest.charge_state(1)
            return

        if  actual_time >=(tTestC2 - tMargin) \
            and actual_time <(tTestC2 + tMargin):
            # print "DISCHARGE,1.0"  Descarga fuerte
            scriptSys.import_data()
            #delay en el inicio de la descarga
            t = scriptSys.TIME_INIT + tTestB2 + 2
            var = scriptSys.get_data('VOLTAGE', \
                range( t - 5 , t - 5 + voltageAverage))
                #promedio de las mediciones al principio
            V1 = sum(var) / float(len(var))
            var = scriptSys.get_data('VOLTAGE', \
                range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
                #promedio de las mediciones al final del test
            V2 = sum(var) / float(len(var))
            var = scriptSys.get_data('CURRENT',
                range(scriptSys.TIME - currentAverage,scriptSys.TIME))
                #promedio de las mediciones al principio
            I1 = sum(var) / float(len(var))
            Z2 = int( ( (float(V2)-float(V1))/float(I1) ) *1000 )
            scriptSys.EVAL['int_z2'] = str(Z2)
            scriptSys.EVAL['int_z'] =   str(Z2) #str(round(Z1,0))
            # chequear rectas
            print "PAUSE"
            return

        if  actual_time >=(tTestB2 - tMargin) \
            and actual_time <(tTestB2 + tMargin):
            # deja reposar y chequea q no caiga la tension
            # stress_test()
            print "DISCHARGE,1.5"
            return

        if  actual_time >= (tTestA2 - tMargin) \
            and  actual_time < (tTestA2 + tMargin) :
            # print "DISCHARGE,0.2"  Descarga suave
            scriptSys.import_data()
            t = scriptSys.TIME_INIT + 2 #delay en el inicio de la descarga
            var = scriptSys.get_data('VOLTAGE', \
                range( t - 5, t- 5 + voltageAverage))
                #promedio de las mediciones al principio
            V1 = sum(var) / float(len(var))
            var = scriptSys.get_data('VOLTAGE', \
                range( scriptSys.TIME - voltageAverage, scriptSys.TIME ))
                #promedio de las mediciones al final del test
            V2 = sum(var) / float(len(var))
            var = scriptSys.get_data('CURRENT', \
                range( scriptSys.TIME - currentAverage,scriptSys.TIME))
                #promedio de las mediciones al principio
            I1 = sum(var) / float(len(var))
            Z1 = int( ( (float(V2)-float(V1))/float(I1) ) *1000 )

            scriptSys.EVAL['int_z1'] =  str(Z1) #str(round(Z1,3))
            # chequear rectas
            print "PAUSE"
            return
        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"measure_z2()")
################################################################
##########                  STRESS                    ##########
################################################################

#Setup
# tTest1  =   20  #tiempo de descarga suave
# tTest2  =   120  #tiempo de descarga fuerte
# tTest3  =   400  #tiempo de recuperacion
# tTest4  =   180 #tiempo de chequeo e incio de sig etapa
# tTest5  =   20
tTest13  =   10  #tiempo de resting
tTest23  =   STRESS_TIME  #tiempo de descarga fuerte
# tTest23  =   30  #tiempo de descarga fuerte 2780
tTest33  =   20  #tiempo de recuperacion
# tTest33  =   10  #tiempo de recuperacion 20
tTest43  =   30 #tiempo de chequeo e incio de sig etapa
tTest53  =   20
vMargin =   16
iMargin =   16
# maxTimeInit = 20          # 10 seg
# voltageAverage = 3
# currentAverage = 5
# Z1 = 0
# Z2 = 0
tTestA3  =   tTest13
tTestB3  =   tTest13 + tTest23
tTestC3  =   tTest13 + tTest23 + tTest33
tTestD3  =   tTest13 + tTest23 + tTest33 + tTest43
iCharge1 =          '0.5'
vCharge1 =          '4.2'
iDischargeTest1 =   '1.8'
# iDischargeTest2 =   '0.5'
iDischargeTest2 =   STRESS_CURRENT
lowVoltageLimit =   2500
tMaxStress =     	2000
# tMaxStress =     	4 * 60 * 60 # 4 hr
maxTimeInit =       	15          # 10 seg
#
def stress_test() :
    try:
        if scriptSys.GENERAL['mode'] != 'STRESS' : #si es llamado por 1
            scriptSys.GENERAL['mode'] = 'STRESS'
            scriptSys.TIME_INIT = scriptSys.TIME
            scriptSys.AUX['testnr'] = str(int(scriptSys.AUX['testnr'])+1)
            scriptSys.AUX['strike'] = 0
            scriptSys.AUX['strikeh'] = 0
            print "PAUSE"
            return
        #condiciones de Fallas:
        if scriptSys.VOLTAGE < lowVoltageLimit : #si actula la proteccion cargo la Batery
            scriptSys.AUX['Dropdown voltage T='+ str(scriptSys.TIME)] =scriptSys.VOLTAGE
            # scriptSys.send_msg('Dropdown voltage T='+ str(scriptSys.TIME))
            scriptSys.final_report("SoHfail",0)
            return
        # if scriptSys.VOLTAGE < vMargin : #si actula la proteccion cargo la Batery
        #     scriptSys.GENERAL['mode'] = 'CHARGE'
        #     scriptSys.TIME_INIT = scriptSys.TIME
        #     print "CHARGE,"+ vCharge1 +","+ iCharge1
        #     return
        if scriptSys.CURRENT > (-iMargin) and scriptSys.VOLTAGE < vMargin :
            scriptSys.AUX['F12'] =scriptSys.CURRENT
            scriptSys.final_report("F12",0)
            return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= maxTimeInit:
            slope1 = scriptSys.get_slope(range(scriptSys.TIME_INIT + 3,scriptSys.TIME))
            if slope1['VOLTAGE']  > 80 and slope1['CURRENT'] > 180 :
                scriptSys.AUX['F13 T='+ str(scriptSys.TIME)] =slope1
                # scriptSys.send_msg('F13 T='+ str(scriptSys.TIME))
                scriptSys.final_report("F13",0)
                return
        if (scriptSys.TIME - scriptSys.TIME_INIT) >= tMaxStress:
            scriptSys.AUX['F12'] =(scriptSys.TIME - scriptSys.TIME_INIT)
            scriptSys.final_report("F15",0)
            return
        ######################################

        actual_time = (scriptSys.TIME - scriptSys.TIME_INIT)
        scriptSys.AUX['actual_time'] = actual_time
        if  actual_time >= (tTestC3- tMargin)and actual_time <(tTestC3 + tMargin):
            msj = evaluate()
            return
        if  actual_time >=(tTestB3 - tMargin)and actual_time <(tTestB3 + tMargin):
            print "PAUSE"
            return
        if  actual_time >=(tTestA3 - tMargin)and actual_time <(tTestA3 + tMargin):
            print "DISCHARGE,"+ iDischargeTest2
            return

        print "RUN"
        return
    except Exception as e:
        scriptSys.error_report(e,"stress_test()")
################################################################
##########                  EVALUATE                  ##########
################################################################
#Setup
Boundary = 70
Bmargin = 5
iDischTest1 =   int(-1000 * float(iDischargeTest1))
iDischTest2 =   int(-1000 * float(iDischargeTest2))
iMar =       60
factor1 = 1             #factores del polinomio ponderado
factor2 = 0
factor3 = 1
factor4 = 15
slopeP   = -194         #pendiente y origen de la regresion lineal
org  = 90000
def evaluate() :
    try:
        scriptSys.import_data()
        flag1 = True
        flag2 = False
        flag3 = False
        flag4 = False
        var = []

        for line in scriptSys.data:
            i = int(line['CURRENT'])
            t = int(line['TIME'])
            s = int(line['STATUS'])
            if s == 3 and flag1 and (t > scriptSys.TIME_INIT):
                flag1 = False
                ind =  scriptSys.data.index(line)
                Vi0 =  int(scriptSys.data[ind+1]['VOLTAGE'])
                Vi0 += int(scriptSys.data[ind+2]['VOLTAGE'])
                Vi0 += int(scriptSys.data[ind+3]['VOLTAGE'])
                Vi0 += int(scriptSys.data[ind+4]['VOLTAGE'])
                Vi0 += int(scriptSys.data[ind+5]['VOLTAGE'])
                Vi0 /= 5 #promedio de las ultimas 5 muestas antes de la descarga
                t0 = int(line['TIME']) #tiempo de inicio de la descarga
                flag2 = True
            if s == 4 and flag2 and (t > scriptSys.TIME_INIT):
                flag2 = False
                ind = scriptSys.data.index(line)
                Vf0 =  int(scriptSys.data[ind-1]['VOLTAGE'])
                Vf0 += int(scriptSys.data[ind-2]['VOLTAGE'])
                Vf0 += int(scriptSys.data[ind-3]['VOLTAGE'])
                Vf0 += int(scriptSys.data[ind-4]['VOLTAGE'])
                Vf0 += int(scriptSys.data[ind-5]['VOLTAGE'])
                Vf0 /= 5 #promedio de las ultimas 5 muestas antes de la descarga

                Vd1 = Vi0 - int(scriptSys.data[ind+0]['VOLTAGE'])
                Vd2 = Vi0 - int(scriptSys.data[ind+16]['VOLTAGE'])
                flag3 = True
            if s == 3 and (t > scriptSys.TIME_INIT): #tomo las tensiones durante la descarga
                var.append(int(line['VOLTAGE']))


        #regresion lineal
        testnr = int(scriptSys.AUX['testnr'])
        if testnr == 1:
            origin = org
        if testnr == 2:
            origin = org - 9000
        if testnr == 3:
            origin = org - 10000
        if testnr == 4:
            origin = org - 10000
        if testnr == 5:
            origin = org - 11000
        result = factor1 * Vd1 + factor2 * Vd2
        SoH = int((result * slopeP + origin)/1000)

        scriptSys.AUX['Vda'+str(testnr)] =Vi0
        scriptSys.AUX['Vdb'+str(testnr)] =Vd1
        scriptSys.AUX['Vdc'+str(testnr)] =Vd2
        scriptSys.AUX['SoH'+str(testnr)] =SoH
        # scriptSys.send_msg('SoH'+str(testnr)+":"+str(SoH))


        ######################################################
        #evaluacion de repetir el test
        # t0 -= len(var)
        ######################################################
        Va = 20         #pico negativo maximo en la descarga
        Vam = 250
        #caso A
        ave = sum(var[5:20])/len(var[5:20])
        t=0
        for  v in var[0:5]:
            t +=1
            if (ave - v) > Va:
                scriptSys.AUX['casoA_t'+str(t0 + t -1)] =(ave - v)
                if int(scriptSys.AUX['strike']) >= 1:
                    if (t0 + t -1)-int(scriptSys.AUX['striket']) >= 30:
                        scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                        scriptSys.AUX['striket'] = str(t0 + t -1)
                else:
                    scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                    scriptSys.AUX['striket'] = str(t0 + t -1)
                # scriptSys.send_msg('casoA  tiempo:  '+ str(t0 + t -1))
            if (ave - v) > Vam:
                scriptSys.AUX['casoAm_t'+str(t0 + t -1)] =(ave - v)
                scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                # scriptSys.send_msg('casoA  tiempo:  '+ str(t0 + t -1))
                scriptSys.final_report("SoHfail",SoH)
                return
        ######################################################
        Vb = 50         #caida promedio maxima en la descarga
        Vbm = 300
        #caso B
        w=10
        t=5
        for x in range(5+w,len(var)-5-w):
            t +=1
            ave = sum(var[x-w:x])/len(var[x-w:x])
            if (ave - var[x])> Vb :
                scriptSys.AUX['casoB_t'+str(t0 + t +w)] =(ave - var[x])
                # scriptSys.send_msg('casoB  tiempo:  '+ str(t0 + t +w))
                if int(scriptSys.AUX['strike']) >= 1:
                    if (t0 + t -1)-int(scriptSys.AUX['striket']) >= 30:
                        scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                        scriptSys.AUX['striket'] = str(t0 + t -1)
                else:
                    scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                    scriptSys.AUX['striket'] = str(t0 + t -1)
            if (ave - var[x])> Vbm :
                scriptSys.AUX['casoBm_t'+str(t0 + t +w)] =(ave - var[x])
                scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                # scriptSys.send_msg('casoB  tiempo:  '+ str(t0 + t +w))
                scriptSys.final_report("SoHfail",SoH)
                return

        ######################################################
        Vc = 20
        Vcm = 200
        #caso C
        ave = sum(var[-25:-5])/len(var[-25:-5])
        t=len(var[:-25])
        for  v in var[-5:]:
            t +=1
            if (ave - v) > Vc:
                scriptSys.AUX['casoC_t'+str(t0 + t -1)] =(ave - v)
                # scriptSys.send_msg('casoC  tiempo:  '+ str(t0 + t -1))
                if int(scriptSys.AUX['strike']) >= 1:
                    if (t0 + t -1)-int(scriptSys.AUX['striket']) >= 30:
                        scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                        scriptSys.AUX['striket'] = str(t0 + t -1)
                else:
                    scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                    scriptSys.AUX['striket'] = str(t0 + t -1)
            if (ave - v) > Vcm:
                scriptSys.AUX['casoCm_t'+str(t0 + t +w)] =(ave - v)
                # scriptSys.send_msg('casoC  tiempo:  '+ str(t0 + t -1))
                scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                scriptSys.final_report("SoHfail",SoH)
                return
        ######################################################
        Vdm = 2800      #tension de caida maxima
        #caso D
        t=0
        for  v in var:
            t +=1
            if v < Vdm:
                scriptSys.AUX['casoDm_t'+str(t0 + t -1)] =v
                # scriptSys.send_msg('casoD  tiempo:  '+ str(t0 + t -1))
                scriptSys.final_report("SoHfail",SoH)
                return

        ######################################################
        #caso E
        p=0         #evaluacion de pendiente positiva
        t=0
        for x in range(20,len(var)-10):
            p +=var[x+1]-var[x]
            t +=1
        if p > 16 :
            # scriptSys.send_msg('casoE  pendiente:  '+ str(p))
            scriptSys.AUX['casoE_t'+str(t0 + t -1)] =p
            if int(scriptSys.AUX['strike']) >= 1:
                if (t0 + t -1)-int(scriptSys.AUX['striket']) >= 30:
                    scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                    scriptSys.AUX['striket'] = str(t0 + t -1)
            else:
                scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                scriptSys.AUX['striket'] = str(t0 + t -1)
        ######################################################
        #casoF
        w=30            #evaluacion de caida de promedio
        t=15
        for x in range(5+w,len(var)-5-w):
            t +=1
            p=0
            for y in range(w):
                p += var[x+y]-var[x+y+1]
                # print var[x]
            if p > 132:
                # scriptSys.send_msg('casoF pendiente:  '+ str(p)+ ' tiempo:  '+ str(t0 + t +w))
                scriptSys.AUX['casoF_t'+str(t0 + t -1)] =p
                if int(scriptSys.AUX['strike']) >= 1:
                    if (t0 + t -1)-int(scriptSys.AUX['striket']) >= 30:
                        scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                        scriptSys.AUX['striket'] = str(t0 + t -1)
                else:
                    scriptSys.AUX['strike'] = str(int(scriptSys.AUX['strike'])+1)
                    scriptSys.AUX['striket'] = str(t0 + t -1)
        ######################################################

        #evaluacion de strikes
        strike = int(scriptSys.AUX['strike'])
        scriptSys.AUX['strikeh'] = int(scriptSys.AUX['strikeh']) + strike
        # if strike >= 3 or strikeh >= 3:
        strikeh = int(scriptSys.AUX['strikeh'])
        #     scriptSys.final_report("SoHfail",SoH)
        if strikeh >=3:
            scriptSys.final_report("SoHfail",SoH)
            return
        #evaluacion de repetir el test
        if testnr >= 2:
            soh1 = int(scriptSys.AUX['soh'+str(testnr-1)])
            # if abs(soh1-int(SoH)) < 20 and strike == 0:
            if abs(int(soh1)-int(SoH)) < 10:
                if  (soh1+int(SoH))/2  > (Boundary + Bmargin):
                    scriptSys.final_report("SoHok",SoH)
                    return
                if (soh1+int(SoH))/2  < (Boundary - Bmargin):
                    scriptSys.final_report("SoHfail",SoH)
                    return
            if testnr >= 5:
                if  (soh1+int(SoH))/2  >= (Boundary):
                    scriptSys.final_report("SoHok",SoH)
                    return
                if (soh1+int(SoH))/2  < (Boundary):
                    scriptSys.final_report("SoHfail",SoH)
                    return

        scriptSys.AUX['strike'] = 0
        scriptSys.TIME_INIT = scriptSys.TIME
        scriptSys.AUX['testnr'] = str(int(scriptSys.AUX['testnr'])+1)
        print "RUN"
        return

    except Exception as e:
        scriptSys.error_report(e,"evaluate()")




################################################################
##########                  ALREADY CHARGED           ##########
################################################################

#Setup
#
def already_charged(option) :
    try:
        if scriptSys.GENERAL['mode'] != 'END' : #si es llamado por primera vez
            scriptSys.GENERAL['mode'] = 'END'
            scriptSys.TIME_INIT = scriptSys.TIME
            print "STOP,NTF,100,0"

        scriptSys.GUI['line1'] = "Analysis Finished"
        if option == 1 :
            scriptSys.GUI['line2'] = "Batery low voltage :" \
                + str(scriptSys.VOLTAGE) + 'V'
        if option == 2 :
            scriptSys.GUI['line2'] = "Batery already DISCHARGED :" \
                + str(scriptSys.VOLTAGE) + 'V'
        scriptSys.GUI['bgcolor'] = '"120,244,183"'
        scriptSys.GUI['extra_info'] = " Z1="+scriptSys.EVAL['int_z1'] \
            +" Z2="+scriptSys.EVAL['int_z2']
        scriptSys.copy_report()
        return
    except Exception as e:
        scriptSys.error_report(e,"already_charged()")
