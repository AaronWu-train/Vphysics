# Filename: vp01.py
# Author: Aaron Wu (B13901011)
# Date: 2020-10-01

from vpython import *

# Constants
g = 9.8  # g = 0.8 m/s^2
size = 0.25  # ball radius
height = 15.0  
py = 3.141593
theta = pi/4
C_drag = 0.9

scene = canvas(align = 'left', center=vec(0, 5, 0), height = 800, width=800, background=vec(0.5, 0.5, 0))
floor = box(length=30, height=0.01, width=4, color=color.blue)
ball = sphere(radius=size, color=color.red, make_trail=1, trail_radius=size / 5)
a1 = arrow(color = color.green, shaftwidth = 0.05)

oscillation = graph(width = 450, align = 'right', center=vec(0, 0, 0))
funct1 = gcurve(graph = oscillation, color=color.blue, width=4)

ball.pos = vec(-15, size, 0)
ball.v =vec(20*cos(theta), 20*sin(theta), 0)

a1.pos = ball.pos
a1.axis = 0.8 * ball.v

touch = 0
dt = 0.001
dis = 0
t = 0

while touch < 3:
    rate(1000)
    ball.v += vec(0, -g, 0) * dt - C_drag * ball.v * dt
    ball.pos += ball.v * dt

    dis += ball.v.mag*dt

    a1.pos = ball.pos
    a1.axis = 0.8*ball.v 
    t += dt
    funct1.plot( pos=(t, ball.v.mag) )
                      
    if ball.pos.y <= size and ball.v.y < 0:
        ball.v.y = -ball.v.y
        touch += 1

msg = text(text = 'displacement = ' + str((ball.pos - vec(-15, size, 0)).x), pos = vec(-10, 7, 0))
msg = text(text = 'total distance = ' + str(dis), pos = vec(-10, -5, 0))



