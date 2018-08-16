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

config = ConfigParser.ConfigParser()

PATH = 'data/st'
if DEBUG_MODE : PATH = '../../data/st'
GENERAL = {}
GUI = {}
EVAL = {}
TIME_INIT = 0
VOLTAGE = 0
CURRENT = 0
TIME = 0
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
        with open(PATH+STATION_N+'.ini', 'w') as configfile:
            config.write(configfile)
        return
    except:
        print "STOP,FAIL,0,0"
        print "Script ERROR:ini_Update()"
################################################################
##########                  ERROR REPORT              ##########
################################################################
def error_report(string):
    try:
        print "STOP,FAIL,0,0"
        print "Script ERROR: " + str(string)
        #
        GUI['line1'] = "Script ERROR"
        GUI['line2'] = "Conflict part :"+ str(string)
        GUI['bgcolor'] = '"244,10,10"'
        GUI['extra_info'] = " TIME="+str(TIME)+" Tinit="+str(TIME_INIT)
        ini_Update()
    except:
        print "error_report() ERROR"
    sys.exit()
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
        #
        return
    except:
        error_report("copy_report()")
################################################################
##########                  FINAL REPORT              ##########
################################################################
#Setup
def final_report(mode, *value) :
    try:
        if GENERAL['mode'] != 'END' : #si es `llamado por primera vez
            GENERAL['mode'] = 'END'
            TIME_INIT = TIME
        if mode == 0 :
            print "STOP,NTF,75,0"
            GUI['line1'] = "Analysis Finished"
<<<<<<< refs/remotes/origin/master
            GUI['line2'] = "Test exit"
            GUI['bgcolor'] = '"120,244,183"'
            GUI['extra_info'] = " Z1="
=======
            GUI['line2'] = "Health: ---    Internal Z: " \
                + str(EVAL['int_z']) + "mOhm"
            GUI['bgcolor'] = '"120,244,183"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']
>>>>>>> Bat Activate
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
            print "STOP,NTF,"+str(value[0])+","+ EVAL['int_z']
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "No trouble found"
            GUI['bgcolor'] = '"120,244,183"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']+" SoH=" + str(value[0])
        if mode == "SoHfail" :
            print "STOP,FAIL,"+str(value[0])+","+ EVAL['int_z']
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "Fail"
            GUI['bgcolor'] = '"120,244,183"'
            GUI['extra_info'] = " Z1="+EVAL['int_z1'] \
                +" Z2="+EVAL['int_z2']+" SoH=" + str(value[0])
        if mode == "sohAW" :
            print "STOP,NTF,"+str(value[0])+","+ EVAL['int_z']
            GUI['line1'] = "Analysis Finished"
            GUI['line2'] = "Health: "+str(value[0])+"    Internal Z: " \
                + str(EVAL['int_z']) + "mOhm"
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
        ini_Update()
        copy_report()
        # return
    except:
        error_report("final_report()")
<<<<<<< refs/remotes/origin/master
    return
=======
    sys.exit()
>>>>>>> Bat Activate
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
        GENERAL['line_b'] = str(holes)
        return
    except:
        error_report("import_data()")
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
    except:
        error_report("get_data()")
################################################################
##########                  get_data                ##########
################################################################
def import_ini( STATION_N ):
    try:
        try: config.read(PATH +STATION_N+".ini")
        except : print "no read .ini"
        sections = config.sections()
        if not 'General' in sections :
            config.add_section('General')
        if not 'GUI' in sections :
            config.add_section('GUI')
        if not 'Eval' in sections :
            config.add_section('Eval')
        options = config.options('General')
        if not 'entradas' in options :
            config.set('General','entradas','0')
        if not 'time' in options :
            config.set('General','time','')
        if not 'machinestatus' in options :
            config.set('General','machinestatus','')
        if not 'mode' in options :
            config.set('General','mode','INIT')
        if not 'time_init' in options :
            config.set('General','time_init','0')
        if not 'voltage' in options :
            config.set('General','voltage','')
        if not 'line_m' in options :
            config.set('General','line_m','')
        if not 'line_b' in options :
            config.set('General','line_b','')
        options = config.options('GUI')
        if not 'line1' in options :
            config.set('GUI','line1','')
        if not 'line2' in options :
            config.set('GUI','line2','')
        if not 'bgcolor' in options :
            config.set('GUI','bgcolor','')
        if not 'extra_info' in options :
            config.set('GUI','extra_info','')
        options = config.options('Eval')
        if not 'int_z2' in options :
            config.set('Eval','int_z2','')
        if not 'int_z1' in options :
            config.set('Eval','int_z1','')
        if not 'health' in options :
            config.set('Eval','health','')
        # config.write(config)
        # config.close()
        with open(PATH + STATION_N + '.ini', 'wb') as configfile:
            config.write(configfile)
        for option in config.options('General'):
            GENERAL[option]=config.get('General',option)
        for option in config.options('GUI'):
            GUI[option]=config.get('GUI',option)
        for option in config.options('Eval'):
            EVAL[option]=config.get('Eval',option)
        return
    except:
        error_report("import_ini()")

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
            last3lines = list(reader)[-3:]
            voltage = int(last3lines[0]['VOLTAGE'])
            voltage += int(last3lines[1]['VOLTAGE'])
            voltage += int(last3lines[2]['VOLTAGE'])
            VOLTAGE = voltage/3
            current = int(last3lines[0]['CURRENT'])
            current += int(last3lines[1]['CURRENT'])
            current += int(last3lines[2]['CURRENT'])
            CURRENT = current/3
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
        ini_Update()
    pass
except:
    print "error con el csv"
    sys.exit()
    pass
