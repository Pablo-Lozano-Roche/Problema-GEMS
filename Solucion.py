# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 09:02:20 2024

@author: pablo
"""
from pulp import *
import json

with open('payload1.json') as file:
  datos=json.load(file)

fuels=datos['fuels']
load=datos['load']
powerplants=datos['powerplants']

gfb1=powerplants[0]
gfb2=powerplants[1]
gfss=powerplants[2]
tj1=powerplants[3]
wp1=powerplants[4]
wp2=powerplants[5]

problema=LpProblem("Problema_Optimización_Recursos",LpMinimize)

p5=fuels['wind(%)']/100*wp1['pmax']
p6=fuels['wind(%)']/100*wp2['pmax']

load=load-(p5+p6)

p1=LpVariable("P1",lowBound=0)
p2=LpVariable("P2",lowBound=0)
p3=LpVariable("P3",lowBound=0)
p4=LpVariable("P4",lowBound=0)
x1=LpVariable("X1",cat='Binary')
x2=LpVariable("X2",cat='Binary')
x3=LpVariable("X3",cat='Binary')



##Función objetivo
problema+= 1/gfb1['efficiency']*fuels['gas(euro/MWh)']*p1+1/gfb2['efficiency']*fuels['gas(euro/MWh)']*p2+1/gfss['efficiency']*fuels['gas(euro/MWh)']*p3+1/tj1['efficiency']*fuels['kerosine(euro/MWh)']*p4+0.3*fuels['co2(euro/ton)']*(p1+p2+p3)    

##Restricciones
problema+= p1+p2+p3+p4==load
problema+= p1<=gfb1['pmax']*x1
problema+= p1>=gfb1['pmin']*x1
problema+= p2<=gfb2['pmax']*x2
problema+= p2>=gfb2['pmin']*x2
problema+= p3<=gfss['pmax']*x3
problema+= p3>=gfss['pmin']*x3
problema+= p4<=tj1['pmax']

problema.solve()
print("La potencia que debe producir cada planta es:\n",gfb1['name'],round(p1.varValue,1),"\n",gfb2['name'],round(p2.varValue,1),"\n",gfss['name'],round(p3.varValue,1),"\n",tj1['name'],round(p4.varValue,1),"\n",wp1['name'],round(p5,1),"\n",wp2['name'],round(p6,1))
