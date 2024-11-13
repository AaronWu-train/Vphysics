from math import pi
from vpython import *

G = 6.6743e-11
mass = {"earth": 5.97e24, "moon": 7.36e22, "sun": 1.99e30}
radius = {
    "earth": 6.371e6 * 10,
    "moon": 1.317e6 * 10,
    "sun": 6.95e8 * 10,
}
earth_orbit = {"r": 1.495e11, "v": 2.9783e4}
moon_orbit = {"r": 3.84e8, "v": 1.022e3}
theta = 5.145 * pi / 180.0


def G_force(m1, m2, pos_vec):
    return -G * m1 * m2 / mag2(pos_vec) * norm(pos_vec)


scene = canvas(
    align="left",
    center=vec(0, -0.5, 0),
    height=900,
    width=900,
    background=vec(0.5, 0.5, 0),
)

textscene = canvas(
    align="right",
    center=vec(0, 0, 0),
    height=500,
    width=500,
    range=250,
    background=vec(0, 0.5, 0.5),
)
# scene.forward = vector(0, -1, 0)

earth_center = -moon_orbit["r"] * mass["moon"] / (mass["earth"] + mass["moon"])
earth_initial_pos = vector(
    earth_center * cos(theta), -earth_center * sin(theta), 0
) + vector(earth_orbit["r"], 0, 0)
earth_initial_v = vector(0, 0, moon_orbit["v"] * mass["moon"] / mass["earth"]) + vector(
    0, 0, -earth_orbit["v"]
)

earth = sphere(
    canvas=scene,
    radius=radius["earth"],
    m=mass["earth"],
    pos=earth_initial_pos,
    v=earth_initial_v,
    texture={"file": textures.earth},
)

moon_center = moon_orbit["r"] * mass["earth"] / (mass["earth"] + mass["moon"])
moon_initial_pos = vector(
    moon_center * cos(theta), -moon_center * sin(theta), 0
) + vector(earth_orbit["r"], 0, 0)
moon_initial_v = vector(0, 0, -moon_orbit["v"]) + vector(0, 0, -earth_orbit["v"])

moon = sphere(
    canvas=scene,
    radius=radius["moon"],
    pos=moon_initial_pos,
    v=moon_initial_v,
    m=mass["moon"],
)

sun = sphere(
    canvas=scene,
    pos=vector(0, 0, 0),
    radius=radius["sun"],
    m=mass["sun"],
    color=color.orange,
    emissive=True,
)

scene.light = []
local_light(pos=vector(0, 0, 0), canvas=scene,)

arrow_moon = arrow(color=color.white, shaftwidth=900000, canvas=scene)
arrow_earth = arrow(color=color.yellow, shaftwidth=500000, canvas=scene)
arrow_earth.axis = vector(0, 2 * radius["earth"], 0)

t = 0
dt = 60 * 60 * 8

record = 0
recorded = False
print_val = 0
text(
    canvas=textscene,
    text="Calculating period of the precession of moon’s orbit:",
    pos=vector(-200, 150, 0),
    height=13,
    color=color.white,
)
textpos = vector(-200, 120, 0)


while True:
    t += dt
    rate(1000)
    moon.a = (
        G_force(mass["moon"], mass["earth"], moon.pos - earth.pos) / mass["moon"]
        + G_force(mass["moon"], mass["sun"], moon.pos - sun.pos) / mass["moon"]
    )
    earth.a = (
        G_force(mass["earth"], mass["moon"], earth.pos - moon.pos) / mass["earth"]
        + G_force(mass["earth"], mass["sun"], earth.pos - sun.pos) / mass["earth"]
    )

    moon.v += moon.a * dt
    moon.pos += moon.v * dt

    earth.v += earth.a * dt
    earth.pos += earth.v * dt

    scene.center = earth.pos
    arrow_moon.pos = earth.pos
    arrow_earth.pos = earth.pos
    arrow_moon.axis = (
        0.3
        * moon_orbit["r"]
        * cross(norm(moon.pos - earth.pos), norm(moon.v - earth.v))
    )

    if (
        arrow_moon.axis.x > 0 and arrow_moon.axis.z < 0 and recorded == False
    ):
        recorded = True
        if record != 0 and (t - record) / 60 / 60 / 24 > 365:
            print(str((t - record) / 60 / 60 / 24) + " days")
            print_str = str((t - record) / 60 / 60 / 24)
            text(
                canvas=textscene,
                text="Period of the precession: " + print_str + " days",
                pos=textpos,
                height=12,
                color=color.white,
            ) 
            textpos += vec(0, -20, 0)
        record = t


    elif arrow_moon.axis.x < 0: 
        recorded = False
