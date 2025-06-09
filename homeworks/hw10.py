from vpython import *
import numpy as np

# -------------------- circuit parameters --------------------
R = 30.0                 # resistance (ohm)
L = 0.200                # inductance (henry)
C = 20e-6                # capacitance (farad)

fd = 120.0               # driving frequency (Hz)
w  = 2 * np.pi * fd
T  = 1 / fd
V0 = 36.0                # source peak voltage (volt)

# -------------------- numerical settings --------------------
t, t_max = 0.0, 20 * T           # simulate 0 ~ 20 T
dt = T / 5000                    # 5 000 steps per cycle

# -------------------- initial state --------------------
i, q = 0.0, 0.0                  # current (A), charge (C)
E0, tao10 = None, None             # energy at 12 T & decay time

# -------------------- graphics --------------------
scene1 = graph(xtitle='t (s)',
               ytitle='i (A)  blue   |  v (V/100)  red',
               background=vector(0.95, 0.97, 0.97), width=600)
scene2 = graph(xtitle='t (s)', ytitle='Energy (J)',
               background=vector(0.95, 0.97, 0.97), width=600)

curve_i = gcurve(color=color.blue,  graph=scene1)
curve_v = gcurve(color=color.red,   graph=scene1)
curve_E = gcurve(color=color.green, graph=scene2)

# -------------------- arrays for 9-th period analysis --------------------
tt9, ii9 = [], []

# -------------------- main loop --------------------
while t < t_max:
    # piece-wise driving voltage
    v_src = V0 * np.sin(w * t) if 0 <= t < 12 * T else 0.0

    # state derivatives (series RLC:  L di/dt + R i + q/C = v(t))
    di_dt = (v_src - R * i - q / C) / L
    dq_dt = i

    # Euler-Cromer integration
    i += di_dt * dt
    q += dq_dt * dt
    t += dt

    # total electromagnetic energy
    E = 0.5 * L * i ** 2 + 0.5 * q ** 2 / C

    # record data for 9-th cycle (8 T ≤ t < 9 T)
    if 8 * T <= t < 9 * T:
        tt9.append(t)
        ii9.append(i)

    # reference energy at switch-off moment (t = 12 T)
    if abs(t - 12 * T) < dt / 2:
        E0 = E

    # find τ when energy decays to 0.1 E₀
    if E0 and tao10 is None and t > 12 * T and E <= 0.1 * E0:
        tao10 = t - 12 * T

    # plotting (thin out points to keep GUI responsive)
    if int(t / dt) % 20 == 0:
        curve_i.plot(t, i)
        curve_v.plot(t, v_src / 100)   # scale voltage for same y-axis
        curve_E.plot(t, E)

# -------------------- post-processing --------------------
# harmonic fit i(t) ≈ a sin wt + b cos wt  ⇒  I = √(a²+b²),  phi = atan2(b, a)
tt9 = np.array(tt9)
ii9 = np.array(ii9)
sinwt = np.sin(w * tt9)
coswt = np.cos(w * tt9)
a = (2 / len(tt9)) * np.sum(ii9 * sinwt)
b = (2 / len(tt9)) * np.sum(ii9 * coswt)
I_num   = np.hypot(a, b)             # numerical amplitude
phi_num   = np.arctan2(b, a)           # rad, current = I sin(wt + phi)

# theoretical steady-state amplitude & phase
Z = complex(R, w * L - 1 / (w * C))
I_theory = V0 / abs(Z)
phi_theory = np.angle(1 / Z)           # current leads v by phi_theory

# -------------------- summary to console --------------------
print('--- 9-th period steady-state comparison ---')
print(f'Numerical  : I = {I_num:.3f} A,  φ = {phi_num:.3f} rad')
print(f'Theoretical: I = {I_theory:.3f} A,  φ = {phi_theory:.3f} rad\n')
print(f'Energy reaches 10 % at τ = {tao10:.4f} s after source off (t = 12 T)')