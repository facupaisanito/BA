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

#####################################################
#####################################################
#Funciones basicas
#####################################################
#####################################################
def ini_Update ():
    for option in GENERAL:
        config.set('General',option,GENERAL[option])
    for option in GUI:
        config.set('GUI',option,GUI[option])
    for option in EVAL:
        config.set('Eval',option,EVAL[option])
    with open('data/st'+STATION_N+'.ini', 'w') as configfile:
        config.write(configfile)
    return
################################################################
##########                  import_data                ##########
################################################################
data = []
def import_data():
    with open("data/st"+STATION_N+".csv",'rb') as f:
        f.readline()
        f.readline()
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if len(data) > 1:
                delta = int(row['TIME']) - int(data[-1]['TIME'])
                if not delta == 1 :
                    i = int(row['CURRENT']) - int(data[-1]['CURRENT']) 
                    data.append(data[-1])
                    data[-1]['TIME'] = str(int(data[-1]['TIME'])+1)
                else:
                    data.append(row)
            else:
                data.append(row)
    return
################################################################
##########                  get_data                ##########
################################################################
def get_data(dType, tLapse):
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
################################################################
##########                  get_data                ##########
################################################################
GENERAL = {}
GUI = {}
EVAL = {}
def import_ini( STATION_N ):
    config.read("data/st"+STATION_N+".ini")
    sections = config.sections()
    if not 'General' in sections :
        config.add_section('General')
    if not 'GUI' in sections :
        config.add_section('GUI')
    if not 'Eval' in sections :
        config.add_section('Eval')
    options = config.options('General')
    if not 'entradas' in options :
        config.set('General','entradas','1')
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
    with open('data/st'+STATION_N+'.ini', 'wb') as configfile:
        config.write(configfile)
    for option in config.options('General'):
        GENERAL[option]=config.get('General',option)
    for option in config.options('GUI'):
        GUI[option]=config.get('GUI',option)
    for option in config.options('Eval'):
        EVAL[option]=config.get('Eval',option)
    return
#####################################################
#####################################################
#Abro el stXX.ini
#####################################################
#####################################################
try:
    import_ini(STATION_N)
    TIME_INIT = int(GENERAL['time_init'])
    # break
except :
    print "ERROR "+"st"+STATION_N+".ini"+ " Not found!! in scriptSys.py"
    sys.exit()
#####################################################
#####################################################
#Abro el stXX.csv
#####################################################
#####################################################
try:
    with open("data/st"+STATION_N+".csv",'rb') as f:
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
            TIME = int(last3lines[2]['TIME'])
            GENERAL['voltage'] = str(voltage/3)     #tension instantanea (en promedio de las ultimas 3 mediciones)
            GENERAL['time'] = last3lines[2]['TIME'] #tiempo en seg de la ultima vez q se tomo registro
        except :
            VOLTAGE = 0
            TIME = 0
            GENERAL['voltage'] = VOLTAGE
            GENERAL['time'] = TIME
        GENERAL['entradas'] = str(int(GENERAL['entradas'])+1)
        ini_Update()
    pass
except:
    print "error con el csv"
    sys.exit()
    pass
