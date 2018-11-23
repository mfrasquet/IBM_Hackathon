#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 00:18:58 2018

@author: miguel
"""

from bokeh.models import BoxAnnotation
from bokeh.plotting import figure, show, output_file
from bokeh.plotting import reset_output
from datetime import datetime
import urllib.request
from bokeh.layouts import gridplot,column
from bokeh.models import SingleIntervalTicker, LinearAxis,FuncTickFormatter, Range1d

with urllib.request.urlopen('https://cosasdejuan.000webhostapp.com/threeroom/api.php') as response:
        html = response.read()
#
        
realdata=[]
temperature=[]
HR=[]
ac=[]
unix=[]
angle=[]
   
sensor=eval(html.decode("utf-8"))
realdata.append(sensor["realdata"])
temperature.append(sensor["temp"])
HR.append(sensor["hum"])
ac.append(sensor["accel"])
unix.append(sensor["unix"])
angle.append(sensor["angle"])


unix_date = [datetime.utcfromtimestamp(i).strftime(' %H:%M:%S') for i in unix[0]]
TOOLS = "pan,box_zoom,reset"

#data = data.loc['2010-10-04':'2010-10-04']

p = figure(y_range=Range1d(0, 4,bounds=(0, 4)),x_range=unix_date,width=800,height=230, tools=TOOLS, title="Aceleración")

p.background_fill_color = "#efefef"
#p.xaxis.axis_label = 'Time'
p.yaxis.axis_label = 'Aceleración [%]'

p.line(list(range(0, len(ac[0]))), ac[0], line_color='grey')
#p.circle(data.index, data.glucose, color='grey', size=1)

p.add_layout(BoxAnnotation(top=0.99, fill_alpha=0.1, fill_color='red', line_color='red'))
p.add_layout(BoxAnnotation(bottom=2.8, fill_alpha=0.1, fill_color='red', line_color='red'))
p.xaxis.major_label_orientation = 3.14/2

p0 = figure(y_range=Range1d(0, 90,bounds=(0, 90)),x_range=p.x_range,width=800,height=230, tools=TOOLS, title="Vuelco")

p0.background_fill_color = "#efefef"
#p.xaxis.axis_label = 'Time'
p0.yaxis.axis_label = 'Vuelco [º]'

p0.line(list(range(0, len(angle[0]))), angle[0], line_color='grey')
#p.circle(data.index, data.glucose, color='grey', size=1)

p0.add_layout(BoxAnnotation(top=0, fill_alpha=0.1, fill_color='red', line_color='red'))
p0.add_layout(BoxAnnotation(bottom=35, fill_alpha=0.1, fill_color='red', line_color='red'))
p0.xaxis.major_label_orientation = 3.14/2


p1 = figure(y_range=Range1d(30, 70,bounds=(30, 70)),x_range=p.x_range,width=800,height=230, tools=TOOLS,title="Humedad Relativa")

p1.background_fill_color = "#efefef"
#p.xaxis.axis_label = 'Time'
p1.yaxis.axis_label = 'Humedad Relativa [%]'

p1.line(list(range(0, len(HR[0]))), HR[0], line_color='grey')
#p.circle(data.index, data.glucose, color='grey', size=1)

p1.add_layout(BoxAnnotation(top=35, fill_alpha=0.1, fill_color='red', line_color='red'))
p1.add_layout(BoxAnnotation(bottom=60, fill_alpha=0.1, fill_color='red', line_color='red'))

#output_file("box_annotation.html", title="box_annotation.py example")

#p.xaxis.ticker = [0,2,4]    
#p.xaxis.major_label_orientation = 3.14/2
p1.xaxis.major_label_orientation = 3.14/2
p2 = figure(y_range=Range1d(-5, 35,bounds=(-5, 35)),x_range=p.x_range,width=800,height=230,tools=TOOLS, title="Temperatura")

p2.background_fill_color = "#efefef"

p2.xaxis.axis_label = 'Time'
p2.yaxis.axis_label = 'Temperatura [ºC]'

p2.line(list(range(0, len(temperature[0]))), temperature[0], line_color='grey')
#p.circle(data.index, data.glucose, color='grey', size=1)

p2.add_layout(BoxAnnotation(top=5, fill_alpha=0.1, fill_color='red', line_color='red'))
p2.add_layout(BoxAnnotation(bottom=30, fill_alpha=0.1, fill_color='red', line_color='red'))
p2.xaxis.major_label_orientation = 3.14/2

show(column(p,p0,p1, p2))
reset_output()