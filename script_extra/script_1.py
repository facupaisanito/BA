import glob
import plotly
import plotly.graph_objs as go
import numpy as np   # So we can use random numbers in examples
import csv
import sys
from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
############################################
# PLOT_DOT = False
PLOT_DOT = True
############################################
layout = dict(
title='Plotter CSV',
xaxis=dict(),
yaxis=dict()
)
#--------------------------------------------------
################################################################
##########                  line1                     ##########
################################################################

#--------------------------------------------------
data = []
info = []
trace = []
Gi = []
VISIBLE = True
i = 0
exito=0
total=0

if len(sys.argv) >= 2 :
    path = sys.argv[1]
    path = path + "*.csv"
else:
    path = "*.csv"
print path
#path = "../../historial/*.csv"
# fig = tools.make_subplots(rows=2, cols=1, subplot_titles=('Current', 'Voltage'),
# shared_xaxes=True , vertical_spacing=0.02 )
for fname in glob.glob(path):
    # print(fname)
    with open(fname,'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        holes = 0
        listax = []
        listay_i = []
        listay_v = []
        listay_r = []
        dot_listax = []
        dot_listay = []
        group = fname[-6:]
        group = group[:-4]
        fname = fname[:-8]
        fname = fname[8:]
        tiempo = 0
        inicio = True
        G = []
        for row in reader: data.append(row)
        for row in data:
            ind = data.index(row) -1
            # if (int(row['CURRENT']) >= -230  and int(row['CURRENT']) <= -170) :
            if (int(row['CURRENT']) >= -1550 and int(row['CURRENT']) <= -1450):
                # lixstay_r.append(str( int(row['CURRENT'])*-1000/float(int(row['VOLTAGE']) )))
                info.append(row)
                var = []
                var.append( int(data[ind+0]['CURRENT'])*-1000/float(int(data[ind+0]['VOLTAGE']) ))
                var.append( int(data[ind+1]['CURRENT'])*-1000/float(int(data[ind+1]['VOLTAGE']) ))
                var.append( int(data[ind+2]['CURRENT'])*-1000/float(int(data[ind+2]['VOLTAGE']) ))
                V1 = sum(var) / float(len(var))
                G.append(V1)
                tiempo += 1
                listay_r.append(str( int(V1) ))
                listax.append(tiempo)

        G.pop()
        G.pop(0)
        listay_r.pop()
        listay_r.pop(0)
        listax.pop()
        listax.pop()

        var = []
        aux = []
        listay_r1 = []
        for i in range(5):
            var.append( int(info[i]['CURRENT'])*-1000/float(int(info[i]['VOLTAGE']) ))
            V1 = int( sum(var) / float(len(var)))
        g0 = int(-1000 * ( int(info[0]['CURRENT'])/float(int(info[0]['VOLTAGE'])) ))
        pen1 =int( 1000*(G[4]-G[0]) )
        #calculo de SoH
        SoH = int(( (pen1 *30)/6000) + 100 )

        aux.append(int(group))
        # aux.append(g0)
        # aux.append(V1)
        # aux.append(pen1)
        aux.append(100*SoH/int(group))
        aux.append(SoH)
        total +=1
        if SoH <= int(group)*1 and SoH >= int(group)*0.8 :
            aux.append("YES")
            exito += 1
        else:    aux.append("NO ")

        Gi.append(aux)
        aux = []
        data = []
        info = []
        G = []



        trace_r = go.Scatter(
        x = listax,
            y = listay_r,
        mode = 'lines',
        legendgroup = group.decode('utf-8', 'ignore'),
        # name = "",
        name = group.decode('utf-8', 'ignore') +'>'+fname.decode('utf-8', 'ignore'),
        showlegend = True ,
        visible = True
        )
        VISIBLE = False
        # fig.append_trace(trace_r, 1, 1)
        # fig.append_trace(trace_i, 1, 1)
        # fig.append_trace(trace_v, 2, 1)
        trace.append(trace_r)
trace.sort()
config = {'scrollZoom': True, 'displayModeBar': True}
plotly.offline.plot(fig, config = config)
# plotly.offline.plot({"data": trace,"layout": layout})
Gi.sort()
for line in Gi:
    print line
print "el exito fue: " + str(100*exito/total)
