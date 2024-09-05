from vpython import *

# Constants
g = 9.8       # g = 0.8 m/s^2
size = 0.25   # ball radius
height = 15.0 # ball canter initial height

# Opening a window
scene = canvas(width = 800, 
               height = 800, 
               center = vec(0, height/2, 0), 
               background = vec(0.5, 0.5, 0))

# Defining objects
floor = box(length = 30, height = 0.01, width = 10, color = color.blue)
ball = sphere(radius = size, color = color.red, make_trail = True, trail_radius = 0.1)

msg = text(text = "Free Fall", pos = vec(-10, 10, 0))

ball.pos = vec(0, height, 0)
ball.v = vec(0, 0, 0)

dt = 0.001
while (ball.pos.y >= size):
    rate(1000)
    ball.pos = ball.pos + (ball.v * dt)
    ball.v.y -= g * dt;

msg.visible = False
msg = text(text = str(ball.v.y), pos = vec(-10, 10, 0))
print(ball.v.y)

exit()


