from vpython import *
from diatomic import *


def handle_collisions(atom1, atom2):
    touched = mag(atom1.pos - atom2.pos) < 2 * size
    approaching = dot(atom1.v - atom2.v, atom1.pos - atom2.pos) < 0
    if touched and approaching:
        atom1.v, atom2.v = collision(atom1, atom2)


N = 20  # 20 molecules
L = ((24.4e-3 / (6e23)) * N) ** (1 / 3.0) / 50
# 2L is the length of the cubic container box, the number is made up
m = 14e-3 / 6e23  # average mass of O and C
k, T = 1.38e-23, 298.0  # some constants to set up the initial speed
initial_v = (3 * k * T / m) ** 0.5  # some constant
scene = canvas(width=400, height=400, align="left", background=vec(1, 1, 1))
container = box(
    length=2 * L, height=2 * L, width=2 * L, opacity=0.4, color=color.yellow
)
energies = graph(width=600, align="left", ymin=0)
c_avg_com_K = gcurve(graph=energies, color=color.green)
c_avg_v_P = gcurve(graph=energies, color=color.red)
c_avg_v_K = gcurve(graph=energies, color=color.purple)
c_avg_r_K = gcurve(graph=energies, color=color.blue)

COs = []

for i in range(N):  # initialize the 20 CO molecules

    # generate one CO molecule
    O_pos = vec(random() - 0.5, random() - 0.5, random() - 0.5) * L
    CO = CO_molecule(pos=O_pos, axis=vector(1.0 * d, 0, 0))

    # set up the initial velocity randomly
    CO.C.v = vector(initial_v * random(), initial_v * random(), initial_v * random())
    CO.O.v = vector(initial_v * random(), initial_v * random(), initial_v * random())

    # store this molecule into list COs
    COs.append(CO)

avg_energies = {"com_K": 0, "v_K": 0, "v_P": 0, "r_K": 0}
plots = {
    "com_K_curve": c_avg_com_K,
    "v_K_curve": c_avg_v_K,
    "v_P_curve": c_avg_v_P,
    "r_K_curve": c_avg_r_K,
}

times = 0  # number of loops that has been run
dt = 5e-16
t = 0

while True:
    rate(3000)
    for CO in COs:
        CO.time_lapse(dt)

    for i in range(N - 1):  # the first N-1 molecules
        for j in range(i + 1, N):
            ## change this to check and handle the collisions between the atoms of different molecules
            # C vs C
            handle_collisions(COs[i].C, COs[j].C)
            handle_collisions(COs[i].O, COs[j].C)
            handle_collisions(COs[i].C, COs[j].O)
            handle_collisions(COs[i].O, COs[j].O)

    for CO in COs:
        # Check the boundary conditions
        for atom in [CO.C, CO.O]:
            for axis in ["x", "y", "z"]:
                if (
                    getattr(atom.pos, axis) < size - L
                    or getattr(atom.pos, axis) > L - size
                ):
                    setattr(atom.v, axis, -getattr(atom.v, axis))

    ## sum com_K, v_K, v_P, and r_K for all molecules, respectively,
    ## to get total_com_K, total_v_K, total_v_P, total_r_K at the current moment

    total_energies = {"com_K": 0, "v_K": 0, "v_P": 0, "r_K": 0}
    for CO in COs:
        total_energies["com_K"] += CO.com_K()
        total_energies["v_K"] += CO.v_K()
        total_energies["v_P"] += CO.v_P()
        total_energies["r_K"] += CO.r_K()

    ## Calculate avg_com_K to be the time average of total_com_K
    ## since the beginning of the simulation, and do the same for others.
    ## Also, plot avg_com_K, avg_v_K, avg_v_P, and avg_r_K
    for key in avg_energies.keys():
        avg_energies[key] = (avg_energies[key] * t + total_energies[key] * dt) / (
            t + dt
        )
        plots[key + "_curve"].plot(t, avg_energies[key])

    t += dt
