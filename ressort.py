from __future__ import division
from matplotlib.backend_bases import key_press_handler
from vpython import *
# Mouvement Harmanic Simple Simulation
l = 5
k = 25 # Constante de raideur du ressort
mass_ = 1
h_box = 1
h_wall = 1.5
floor1 = box(pos=vector(0, -1, 0), length=l, width=0.5, height=0.1, color=color.green)
wall = box(pos=vector(-l/2, -0.5-0.05, 0), length=0.1, width=0.5, height=1, color=color.green)
mass = box(pos=vector(l/8, -0.5-0.05, 0), length=1.125, width=0.5, height=1, color=color.gray(0.5), opacity=0.3)
ressort = helix(pos=wall.pos+vector(+l/64, 0, 0), axis=vector(0.5, 0, 0), radius=0.3, coils=10, height=0.5, length=l/2, color=color.cyan)
weight_pointer = arrow(pos=mass.pos, axis=vector(0, -1.5, 0), color=color.red, opacity=0.5)
normal_pointer = arrow(pos=mass.pos, axis=vector(0, 1.5, 0), color=color.yellow, opacity=0.5)
normal_pointer.pos.y = -1-0.05
# Creating the graph
g = graph()
g2 = graph()
x_plot = gcurve(graph=g, color=color.red, label="x") #Position
v_plot = gcurve(graph=g, color=color.green, label="v") #Velocity
a_plot = gcurve(graph=g, color=color.blue, label="a") #acceleration

V_plot = gcurve(graph=g2, color=color.green, label="VE") #Potential Energy
ke_plot = gcurve(graph=g2, color=color.red, label="KE") #Kinetic Energy
E_plot = gcurve(graph=g2, color=color.blue, label="E") #Total Energy

t = 0
while True:
    rate(10)
    if cos(t) > 0:
        mass.pos.x = mass.pos.x + cos(t)/20
    else:
        mass.pos.x = mass.pos.x + cos(t)/20 
        if mass.pos.x < l/8:
            mass.pos.x = l/8
        
    ressort.length = l/2+mass.pos.x
    weight_pointer.pos = mass.pos
    normal_pointer.pos.x = mass.pos.x
    x_plot.plot(t, cos(0.49*t) * (1/20)) # w = 0.49
    v_plot.plot(t, sin(0.49*t) * (-1/20) * 0.49) # w = 0.49
    a_plot.plot(t, cos(0.49*t) * (-1/20) * 0.49**2) # w = 0.49
    V_plot.plot(t, (1/2)*k*0.05**2*cos(0.49*t)**2)
    ke_plot.plot(t, (1/2)*k*0.05**2*sin(0.49*t)**2)
    E_plot.plot(t, (1/2)*k*0.05**2)
    t +=0.1