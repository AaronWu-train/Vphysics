from vpython import *

# Constants
g = vector(0, -9.8, 0)
k = 150000
size, m = 0.2, 1
L = 2  # length = 2.00 m

N = 2

scene = canvas(
    align="left",
    center=vec(0, -0.5, 0),
    height=600,
    width=600,
    background=vec(0.5, 0.5, 0),
)
ceiling = box(length=5, height=0.005, width=5, color=color.green, pos=vec(0, 0, 0))

springs = []
for i in range(5):
    spring = cylinder(radius=0.005, pos=vec(0.4 * i - 1, 0, 0))
    springs.append(spring)

balls = []
for i in range(5):
    ball = sphere(pos=vec(0.4 * i - 1, -L, 0), radius=size, color=color.red)
    ball.v = vec(0, 0, 0)
    ball.m = m
    balls.append(ball)


for i in range(N):
    balls[i].pos = vec(-sqrt(2**2 - 1.95**2) + 0.4 * i - 1, -1.95, 0)

# plot 1
instant_plot = graph(width=400, align="left", xtitle="Time (s)", ytitle="Energy (J)")
k_plot = gcurve(
    graph=instant_plot, color=color.blue, width=2.5, label="kinetic energy", legend=True
)
p_plot = gcurve(
    graph=instant_plot,
    color=color.orange,
    width=2.5,
    label="potential energy",
    legend=True,
)

# plot 2
average_plot = graph(width=400, align="left", xtitle="Time (s)", ytitle="Energy (J)")
avg_k_plot = gcurve(
    graph=average_plot,
    color=color.blue,
    width=2.5,
    label="average kinetic energy",
    legend=True,
)
avg_p_plot = gcurve(
    graph=average_plot,
    color=color.orange,
    width=2.5,
    label="average potential energy",
    legend=True,
)
avg_k = 0
avg_p = 0


t = 0
dt = 0.0001

while True:
    rate(5000)
    t += dt
    ke = 0
    pe = 0
    for i in range(5):
        springs[i].axis = balls[i].pos - springs[i].pos
        spring_force = -k * (mag(springs[i].axis) - L) * springs[i].axis.norm()
        balls[i].a = g + spring_force / m
        balls[i].v += balls[i].a * dt
        balls[i].pos += balls[i].v * dt
        if (
            i < 4
            and 0.4 >= mag(balls[i].pos - balls[i + 1].pos)
            and dot(balls[i].pos - balls[i + 1].pos, balls[i].v - balls[i + 1].v) <= 0
        ):
            balls[i].v, balls[i + 1].v = balls[i + 1].v, balls[i].v

        ke += 0.5 * balls[i].m * mag2(balls[i].v)
        pe += m * 9.8 * (balls[i].pos.y + 2)

    k_plot.plot(pos=(t, ke))
    p_plot.plot(pos=(t, pe))

    avg_k = (avg_k * (t - dt) + ke * dt) / t
    avg_p = (avg_p * (t - dt) + pe * dt) / t
    avg_k_plot.plot(pos=(t, avg_k))
    avg_p_plot.plot(pos=(t, avg_p))
