#-----------------------------------------------------------------------
# ScriptSys  for BA
# Version: 1
# Compatible with HW:
# Developed by Ignacio Cazzasa and company for CWG
#-----------------------------------------------------------------------
DEBUG_MODE = False
try:
    import sys,os
except:
    print "import sys,os in scriptSys Not found!!"
    sys.exit()
try:
    import ConfigParser
except:
    print "import configparser in scriptSys Not found!!"
    sys.exit()
try:
    import csv
except:
    print "import CSV in scriptSys Not found!!"
    sys.exit()
for px in sys.argv:
    if px == '-d':
        DEBUG_MODE = True
        try:
            sys.argv.append('--Param-scriptDebug')
            sys.argv.append(sys.argv[1])
            import scriptDebug
        except:
            print "ERROR file scriptDebug Not found!!"
            sys.exit()
for px in sys.argv:
    if px == '--Param-scriptSys':
        idx = sys.argv.index(px)
        sys.argv.pop(idx) # remove option
        STATION_N = sys.argv[idx]
        sys.argv.pop(idx) # remove value

config = ConfigParser.SafeConfigParser()

PATH = 'data/st'
if DEBUG_MODE : PATH = '../../data/st'
GENERAL = {}
GUI = {}
EVAL = {}
MENSSAGE = {}
AUX = {}
TIME_INIT = 0
VOLTAGE = 0
CURRENT = 0
TIME = 0
Msg = 0
#####################################################
#####################################################
#Funciones basicas
#####################################################
#####################################################
def ini_Update ():
    try:
        GENERAL['time'] = str(TIME)
        GENERAL['time_init'] = str(TIME_INIT)
        GENERAL['voltage'] = str(VOLTAGE)
        for option in GENERAL:
            config.set('General',option,GENERAL[option])
        for option in GUI:
            config.set('GUI',option,GUI[option])
        for option in EVAL:
            config.set('Eval',option,EVAL[option])
        for option in MENSSAGE:
            config.set('Msg',option,MENSSAGE[option])
        for option in AUX:
            config.set('AUX',option,AUX[option])
        with open(PATH+STATION_N+'.ini', 'w') as configfile:
            config.write(configfile)
            configfile.close()

        return
    except Exception as e:
        # print "STOP,FAIL,0,0"
        print "Script ERROR:ini_Update()"
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    return
################################################################
##########                  ERROR REPORT              ##########
################################################################
def error_report(e,string):
    try:
        print "STOP"

        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        # print "Script ERROR: " + str(string)
        # err = str('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        #
        GUI['line1'] = "Script ERROR: "+ str(string)
        GUI['line2'] = ""
        GUI['bgcolor'] = '"244,10,10"'
        GUI['extra_info'] = " TIME="+str(TIME)+" Tinit="+str(TIME_INIT)
        ini_Update()
    except Exception as e:
        print "error_report() ERROR"
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    return
################################################################
##########                  COPY REPORT               ##########
################################################################
def copy_report() :
    try:
        try:
            with open(PATH + STATION_N + ".csv", "rb") as ifile:
                ifile.readline()
                name = ifile.readline()
                name = name.replace(" ","_")
                name = name.replace(",","_")
                name = name.replace(".","")
                name = name.replace(":","-")
                name = name[:-12]
                reader = csv.reader(ifile)
                dato = []
                for row in reader:
                    dato.append(row)
            ifile.close()
        except:
            print "el copy no funciono csv1"
        file_path = "historial/"+ name
        directory = os.path.dirname(file_path)
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)
        try:
            myFile = open( file_path +".csv", 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(dato)
            myFile.close()
        except:
            print "Create /historal folder!!!"
        try:
            with open(PATH + STATION_N + ".ini", "rb") as ifile:
                reader = csv.reader(ifile)
                dato = []
                for row in reader:
                    dato.append(row)
            ifile.close()
        except:
            print "el copy no funciono csv1"
        try:
            myFile = open(file_path +".ini", 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(dato)
            myFile.close()
        except:
            print "el copy no funciono csv2"
        try:
            with open(PATH + STATION_N + ".log", "rb") as ifile:
                reader = csv.reader(ifile)
                dato = []
                for row in reader:
                    dato.append(row)
            ifile.close()
        except:
            print "lectura del log fallo"
        try:
            myFile = open(file_path +".log", 'w')
            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(dato)
            myFile.close()
        except:
            print "escritura del log fallo"
        #
        return
    except Exception as e:
        error_report(e,"copy_report()")
################################################################
##########                  SEND MESSAGE              ##########
################################################################
def send_msg(string) :
    try:
        MENSSAGE['type'] = "warning"
        MENSSAGE['time'] = "60"
        MENSSAGE['txt'] = string
        # return
        ini_Update()
        return
    except Exception as e:
        error_report(e,"send_msg()")
################################################################
##########                  FINAL REPORT              ##########
################################################################
def final_report(mode, *value) :
    try:
        if mode == 0 :
            print "STOP,NTF,75,0"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "Health: ---    Internal Z: " \
                + str(EVAL['int_z']) + "mOhm"
            GUI['bgcolor'] = '"120,244,183"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']
        if mode == "soh" :
            print "STOP,NTF,"+str(value[0])+","+ EVAL['int_z']
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "Health: "+str(value[0])+"    Internal Z: " \
                + str(EVAL['int_z']) + "mOhm"
            GUI['bgcolor'] = '"120,244,183"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']+" SoH=" + str(value[0])
        if mode == "maxTimeCharge" :
            GENERAL['mode']= "STOP"
            print "STOP"
            GUI['line1'] = "Analysis Stopped"
            GUI['line2'] = "Max time of CHARGE reached"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "This is scriptTest.py"
        if mode == "maxTimeDischarge" :
            TIME_INIT = TIME
            GENERAL['mode']= "STOP"
            print "STOP"
            GUI['line1'] = "Analysis Stopped"
            GUI['line2'] = "Max time of DISCHARGE reached"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "This is scriptTest.py"
        if mode == "SoHok" :
            print "STOP,NTF,0,0"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "No trouble found" #+" :"+str(value[0])+"%"
            GUI['bgcolor'] = '"20,178,120"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']+" SoH=" + str(value[0])
        if mode == "SoHfail" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "Fail "#+" :"+str(value[0])+"%"
            GUI['bgcolor'] = '"237,55,82"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']+" SoH=" + str(value[0])
        if mode == "sohAW" :
            print "STOP,NTF,"+str(value[0])+","+ EVAL['int_z']
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "Health: "+str(value[0])+" Ah: " \
                + str(value[1]) + " Wh:"+ str(value[2])
            GUI['bgcolor'] = '"120,244,183"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']+" SoH=" + str(value[0])
        if mode == "maxTimeInitFail" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "maxTimeInitFail Finished"
            GUI['line2'] = "Health: "+str(value[0])+"    Internal Z: " \
                + str(EVAL['int_z']) + "mOhm"
            GUI['bgcolor'] = '"120,244,183"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']+" SoH=" + str(value[0])

        if mode == "F01" : #Presencia de corriente en estado de reposo
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F01"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F02" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F02"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F03" : #En charge_state no toma caarga o V<Vcharge-100mv
            print "STOP,0,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F03"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F04" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F04"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F05" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F05"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F06" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F06"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F07" : #charge_state Pendiente tension positiva y corriente negativo
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F07"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F08" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F08"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F09" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F09"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F10" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F10"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F11" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F11"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F12" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F12"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F13" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F13"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F14" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F14"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F15" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F15"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F16" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F16"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F17" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F17"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F18" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F18"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F19" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F019"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F20" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F20"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F21" :
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Error n F21"
            GUI['bgcolor'] = '"244,0,0"'
            GUI['extra_info'] = "none"
        if mode == "F22" : #bateria desconectada
            print "STOP,FAIL,0,0"
            GUI['line1'] = "Analysis Fail"
            GUI['line2'] = "Battery disconected"
            GUI['bgcolor'] = '"227,123,64"'
            GUI['extra_info'] = "none"
            GUI['extra_info'] = "none"
            MENSSAGE['type'] = "warning"
            MENSSAGE['time'] = "60"
            MENSSAGE['txt'] = "Battery disconected"
        # return
    except Exception as e:
        error_report(e,"final_report()")
    ini_Update()
    copy_report()
    return
################################################################
##########                  import_data                ##########
################################################################
data = []
def import_data():
    try:
        with open(PATH +STATION_N+".csv",'rb') as f:
            f.readline()
            f.readline()
            reader = csv.DictReader(f, delimiter=',')
            holes = 0
            for row in reader: data.append(row)
            for row in data:
                ind = data.index(row) + 1
                if row['TIME'] == data[-1]['TIME'] : break
                delta = int(data[ind]['TIME']) - int(row['TIME'])
                deltaV = int(data[ind]['VOLTAGE']) - int(row['VOLTAGE'])
                deltaI = int(data[ind]['CURRENT']) - int(row['CURRENT'])
                deltaT = int(data[ind]['TEMP']) - int(row['TEMP'])
                if delta > 1:
                    holes = holes + 1
                    dV=deltaV/delta
                    dI=deltaI/delta
                    dT=deltaT/delta
                    temp = {}
                    for x in row:
                        temp[x] = row[x]
                    temp['TIME'] = str(int(row['TIME'])+1)
                    temp['VOLTAGE'] = str(int(row['VOLTAGE'])+dV)
                    temp['CURRENT'] = str(int(row['CURRENT'])+dI)
                    temp['TEMP'] = str(int(row['TEMP'])+dT)
                    data.insert(ind,temp)
        AUX['line_b'] = str(holes)
        return
    except Exception as e:
        error_report(e,"import_data()")
################################################################
##########                  get_data                ##########
################################################################
def get_data(dType, tLapse):
    try:
        if len(data) <= 1 :
            import_data()   #Comprueba que este cargado el csv

        if 'list' in str(type(tLapse)):
            info = []
            for x in tLapse :
                var = [int(row[dType]) for row in data if int(row['TIME']) == x]
                info.append(var[0])
        else :
            info = [int(row[dType]) for row in data if int(row['TIME']) == tLapse]
            return info[0]
        return info
    except Exception as e:
        error_report(e,"get_data()")
################################################################
##########                  get_slope                ##########
################################################################
def get_slope(tLapse):
    try:
        v = get_data("VOLTAGE",tLapse)
        i = get_data("CURRENT",tLapse)
        t = get_data("TEMP",tLapse)
        dI1 =0
        for a in range(len(i)-1):
            dI1 += i[a+1] - i[a]
        iSlope = ( 1000* dI1) / len(i)
        dV1 =0
        for a in range(len(v)-1):
            dV1 += v[a+1] - v[a]
        vSlope = ( 1000* dV1) / len(v)
        dt1 =0
        for a in range(len(t)-1):
            dt1 += t[a+1] - t[a]
        tSlope = ( 1000* dt1) / len(t)
        slope = {"VOLTAGE":vSlope ,"CURRENT": iSlope ,"TEMP": tSlope}

        #############
        # sys.stdout=open("output.txt","w")
        # print "t:"+str(TIME)
        # print v
        # print tLapse
        # print slope
        # sys.stdout.close()
        ##########################
        return slope
    except Exception as e:
        scriptSys.error_report(e,"get_slope()")
################################################################
##########                  get_data                ##########
################################################################
def import_ini( STATION_N ):
    try:
        try: config.read(PATH +STATION_N+".ini")
        except Exception as e:
            print "config.read(configfile) ERROR"
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        # sections = config.sections()
        try:
            for option in config.options('General'):
                GENERAL[option]=config.get('General',option)
            for option in config.options('GUI'):
                GUI[option]=config.get('GUI',option)
            for option in config.options('Eval'):
                EVAL[option]=config.get('Eval',option)
            for option in config.options('Msg'):
                MENSSAGE[option]=config.get('Msg',option)
            for option in config.options('AUX'):
                AUX[option]=config.get('AUX',option)
        except:
            if not config.has_section('General'):
                config.add_section('General')
            if not config.has_option('General', 'entradas'):
                config.set('General','entradas','0')
            if not config.has_option('General', 'time'):
                config.set('General','time','')
            if not config.has_option('General', 'machinestatus'):
                config.set('General','machinestatus','')
            if not config.has_option('General', 'mode'):
                config.set('General','mode','INIT')
            if not config.has_option('General', 'time_init'):
                config.set('General','time_init','0')
            if not config.has_option('General', 'voltage'):
                config.set('General','voltage','')
            if not config.has_option('General', 'vstate'):
                config.set('General','vstate','')

            if not config.has_section('GUI'):
                config.add_section('GUI')
            if not config.has_option('GUI', 'line1'):
                config.set('GUI','line1','')
            if not config.has_option('GUI', 'line2'):
                config.set('GUI','line2','')
            if not config.has_option('GUI', 'bgcolor'):
                config.set('GUI','bgcolor','')
            if not config.has_option('GUI', 'extra_info'):
                config.set('GUI','extra_info','')

            if not config.has_section('Eval'):
                config.add_section('Eval')
            if not config.has_option('Eval', 'int_z2'):
                config.set('Eval','int_z2','')
            if not config.has_option('Eval', 'int_z1'):
                config.set('Eval','int_z1','')
            if not config.has_option('Eval', 'health'):
                config.set('Eval','health','')

            if not config.has_section('Msg'):
                config.add_section('Msg')
            if not config.has_option('Msg', 'type'):
                config.set('Msg','type','')
            if not config.has_option('Msg', 'time'):
                config.set('Msg','time','')
            if not config.has_option('Msg', 'txt'):
                config.set('Msg','txt','')

            if not config.has_section('AUX'):
                config.add_section('AUX')
            if not config.has_option('AUX', 'line_m'):
                config.set('AUX','line_m','')
            if not config.has_option('AUX', 'line_b'):
                config.set('AUX','line_b','')
            if not config.has_option('AUX', 'testnr'):
                config.set('AUX','testnr','0')
            try:
                with open(PATH + STATION_N + '.ini', 'w') as configfile:
                    config.write(configfile)
                    configfile.close()
            except Exception as e:
                print "config.write(configfile) ERROR"
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        # config.write(config)
        # config.close()

        return
    except Exception as e:
        error_report(e,"import_ini()")
#####################################################
#####################################################
##      Abro el stXX.ini                           ##
#####################################################
#####################################################
try:
    import_ini(STATION_N)
    try :   TIME_INIT = int(GENERAL['time_init'])
    except : TIME_INIT = 0

except :
    print "ERROR "+"st"+STATION_N+".ini"+ " Not found!! in scriptSys.py"
    sys.exit()
#####################################################
#####################################################
##      Abro el stXX.csv                          ##
#####################################################
#####################################################
try:
    with open(PATH + STATION_N + ".csv",'rb') as f:
        f.readline()
        f.readline()
        reader = csv.DictReader(f, delimiter=',')
        header = reader.fieldnames
        try:
            try:
                lastlines = list(reader)[-10:]
            except :
                lastlines = list(reader)[-9:]
            last3lines = lastlines
            voltage = int(last3lines[0]['VOLTAGE'])
            voltage += int(last3lines[1]['VOLTAGE'])
            voltage += int(last3lines[2]['VOLTAGE'])
            VOLTAGE = voltage/3
            # current = int(last3lines[0]['CURRENT'])
            # current += int(last3lines[1]['CURRENT'])
            # current += int(last3lines[2]['CURRENT'])
            # CURRENT = current/3
            CURRENT += int(last3lines[2]['CURRENT'])
            TIME = int(last3lines[2]['TIME'])
            GENERAL['voltage'] = str(voltage/3)
            #tension instantanea (en promedio de las ultimas 3 mediciones)
            GENERAL['time'] = last3lines[2]['TIME']
            #tiempo en seg de la ultima vez q se tomo registro
        except :
            CURRENT = 0
            VOLTAGE = 0
            TIME = 0
            GENERAL['voltage'] = VOLTAGE
            GENERAL['time'] = TIME
        if TIME <= 15 : #asume primera entrada
            GENERAL['entradas'] = '0'
            GENERAL['mode'] = 'INIT'
            TIME_INIT = 0
            EVAL['int_z'] = ''
            EVAL['int_z1'] = ''
            EVAL['int_z2'] = ''
            EVAL['health'] = ''
            GUI['line1'] = ''
            GUI['line2'] = ''
            GUI['bgcolor'] = ''
            GUI['extra_info'] = ''

        try :    GENERAL['entradas'] = str(int(GENERAL['entradas'])+1)
        except : GENERAL['entradas'] = "1.0"

        # with open(PATH + STATION_N + ".csv",'rb') as f:
        #     f.readline()
        #     f.readline()
        #     reader = csv.DictReader(f, delimiter=',')
        # header = reader.fieldnames
        try:
            # print list(reader)
            # print list(reader)[-5:]
            if TIME < 10:
                for i in range(5):
                    if int(lastlines[i]['MSG']) == 81:
                        Msg =81
            else:
                for i in range(10):
                    if int(lastlines[i]['MSG']) == 81:
                        Msg = 81
        except Exception as e:
            # print "STOP,FAIL,0,0"
            print "Script ERROR:ini_Update()"
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

        ini_Update()
    pass
except:
    print "error con el csv desde scriptSys"
    sys.exit()
    pass
