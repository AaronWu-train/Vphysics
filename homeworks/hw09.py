# Mutual inductance between two coaxial circular loops
import numpy as np, math, time

MU0 = 4 * math.pi * 1e-7   # vacuum permeability (H/m)
I   = 1.0                  # test current (A)

# --- geometry (meters) ---
R_big   = 0.12             # radius of loop on z = 0       (large loop)
R_small = 0.06             # radius of loop on z = H_sep   (small loop)
H_sep   = 0.10             # vertical separation

def mutual_inductance(radius_src, radius_dst, height,
                      n_seg=1200, n_rings=120, n_phi=240):
    """Flux through dst-loop caused by 1 A on src-loop (Biot-Savart)."""
    # cut source loop into n_seg pieces
    theta = np.linspace(0.0, 2*math.pi, n_seg, endpoint=False)
    dtheta = 2*math.pi / n_seg
    x_seg, y_seg = radius_src * np.cos(theta), radius_src * np.sin(theta)
    dl_x = -radius_src * np.sin(theta) * dtheta
    dl_y =  radius_src * np.cos(theta) * dtheta

    # partition destination area into concentric rings
    rho_edges = np.linspace(0.0, radius_dst, n_rings + 1)
    flux = 0.0

    for i in range(n_rings):                       # sum rings
        rho_mid = 0.5 * (rho_edges[i] + rho_edges[i+1])
        area_ring = math.pi * (rho_edges[i+1]**2 - rho_edges[i]**2)

        # average B_z over the ring with angular samples
        phi = np.linspace(0.0, 2*math.pi, n_phi, endpoint=False)
        bz_sum = 0.0
        for ang in phi:                            # sum over ds
            x_p = rho_mid * math.cos(ang)
            y_p = rho_mid * math.sin(ang)
            z_p = height                          # dst loop plane

            # vector r from each segment to field point
            rx, ry = x_p - x_seg, y_p - y_seg
            r_sq = rx*rx + ry*ry + z_p*z_p

            # z-component of dl × r
            cp_z = dl_x * ry - dl_y * rx
            bz_sum += np.sum(cp_z / r_sq**1.5)

        bz_avg = (MU0 / (4*math.pi)) * (bz_sum / n_phi)
        flux  += bz_avg * area_ring

    return flux / I                               # mutual M

t0 = time.time()
M_big_to_small = mutual_inductance(R_big,   R_small,  H_sep)   # (1)
M_small_to_big = mutual_inductance(R_small, R_big,   -H_sep)   # (2)
percent_diff = abs(M_big_to_small - M_small_to_big) / M_big_to_small * 100.0

print(f"M_big_to_small  = {M_big_to_small*1e9:.6f} nH")
print(f"M_small_to_big  = {M_small_to_big*1e9:.6f} nH")
print(f"Percent diff    = {percent_diff:.6f} %   (runtime {time.time()-t0:.2f} s)")