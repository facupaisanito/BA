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
data = []
info = []
VISIBLE = True
path = "*.csv"
# path = "../../historial/*.csv"
fig = tools.make_subplots(rows=2, cols=1, subplot_titles=('Current', 'Voltage'),
shared_xaxes=True , vertical_spacing=0.02 )
for fname in glob.glob(path):
    # print(fname)
    with open(fname,'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        holes = 0
        dot_listax = []
        dot_listay = []
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
                    dot_listax.append(str(int(row['TIME'])+1))
                    dot_listay.append(0)
                    temp['TIME'] = str(int(row['TIME'])+1)
                    temp['VOLTAGE'] = str(int(row['VOLTAGE'])+dV)
                    temp['CURRENT'] = str(int(row['CURRENT'])+dI)
                    temp['TEMP'] = str(int(row['TEMP'])+dT)
                    data.insert(ind,temp)
        reader = csv.DictReader(f, delimiter=',')
        header = reader.fieldnames
        listax = []
        listay_i = []
        listay_v = []
        for row in data:
            listax.append(row["TIME"])
            listay_i.append(row["CURRENT"])
            listay_v.append(row["VOLTAGE"])
        data = []
        fname = fname[:-8]
        fname = fname[16:]

        trace_i = go.Scatter(
        x = listax,
        y = listay_i,
        mode = 'lines',
        name = "I :" + fname.decode('utf-8', 'ignore'),
        visible = VISIBLE
        )
        trace_v = go.Scatter(
        x = listax,
        y = listay_v,
        mode = 'lines',
        name = "V :" + fname.decode('utf-8', 'ignore'),
        visible = VISIBLE
        )
        # VISIBLE = False
        fig.append_trace(trace_i, 1, 1)
        fig.append_trace(trace_v, 2, 1)
        # info.append(trace)
        if PLOT_DOT :
            dot_trace = go.Scatter(
            x = dot_listax,
            y = dot_listay,
            mode = 'markers',
            name = fname.decode('utf-8', 'ignore') + "_dot"
            )
            fig.append_trace(dot_trace, 1, 1)
config = {'scrollZoom': True, 'displayModeBar': True}
plotly.offline.plot(fig, config = config)

# plotly.offline.plot({"data": info,"layout": layout})



#
# from plotly import tools
# import plotly.plotly as py
# import plotly.graph_objs as go
#
# trace1 = go.Scatter(
#     x=[0, 1, 2],
#     y=[10, 11, 12]
# )
# trace2 = go.Scatter(
#     x=[2, 3, 4],
#     y=[100, 110, 120],
# )
# trace3 = go.Scatter(
#     x=[3, 4, 5],
#     y=[1000, 1100, 1200],
# )
#
# fig = tools.make_subplots(rows=2, cols=1)
#
# fig.append_trace(trace3, 1, 1)
# fig.append_trace(trace2, 2, 1)
#
# plotly.offline.plot(fig)
