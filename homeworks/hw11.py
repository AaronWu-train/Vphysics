from vpython import *

# Scene and lens geometry -----------------------------------------------------
scene = canvas(background=vec(0.8, 0.8, 0.8),
               width=1200, height=300,
               center=vec(3, 0, 10), fov=0.004)

lens_surface1 = shapes.arc(radius=0.15, angle1=0,   angle2=pi)
lens_surface2 = shapes.arc(radius=0.15, angle1=-pi, angle2=0)
circle_path   = paths.arc(pos=vec(0, 0, 0), radius=1e-7,
                          angle2=2*pi, up=vec(1, 0, 0))

extrusion(path=circle_path, shape=lens_surface1,
          color=color.yellow, opacity=0.6)
extrusion(path=circle_path, shape=lens_surface2,
          color=color.yellow, opacity=0.6)

curve(pos=[vec(-7, 0, 0), vec(13, 0, 0)],
      color=color.red, radius=0.02)                    # optical axis
arrow(pos=vec(-6, 0, 0),  axis=vec(0,  0.5, 0),
      shaftwidth=0.1, color=color.green)               # object
arrow(pos=vec(12, 0, 0), axis=vec(0, -1.0, 0),
      shaftwidth=0.1, color=color.black)               # image plane

# Snell-law refraction --------------------------------------------------------
def refraction_vector(n1: float, n2: float, v_in: vector, n: vector) -> vector:
    v_in = norm(v_in)
    n    = norm(n)
    if dot(v_in, n) > 0:
        n = -n                                           # flip if needed

    cos_i = -dot(n, v_in)
    eta   = n1 / n2
    k     = 1 - eta**2 * (1 - cos_i**2)

    if k < 0:                                            # TIR
        return norm(v_in + 2 * cos_i * n)

    cos_t = sqrt(k)
    return norm(eta * v_in + (eta * cos_i - cos_t) * n)

print(refraction_vector(1, 1.5, norm(vec(-1, 1, 0)), norm(vec(0, 1, 0))))
# Lens parameters -------------------------------------------------------------
R          = 4.0        # surface radius of curvature (cm)
thickness  = 0.3        # lens center thickness (cm)
g1center   = vec(-R + thickness/2, 0, 0)   # exit surface center
g2center   = vec( R - thickness/2, 0, 0)   # entry surface center

n_air   = 1.0
n_glass = 1.5

# Ray tracing -----------------------------------------------------------------
for angle in range(-7, 2):                       # nine rays
    ray = sphere(pos=vec(-6, 0.5, 0),
                 radius=0.01, color=color.blue,
                 make_trail=True)
    ray.v    = vector(cos(angle / 40.0), sin(angle / 40.0), 0)
    medium   = "air"
    dt       = 0.002

    while True:
        rate(1000)
        ray.pos += ray.v * dt

        # entry surface (air → glass)
        if medium == "air" and ray.pos.x >= -thickness / 2:
            n      = norm(g2center - ray.pos)
            ray.v  = refraction_vector(n_air, n_glass, ray.v, n)
            medium = "glass"
            continue

        # exit surface (glass → air)
        if medium == "glass" and ray.pos.x >= thickness / 2:
            n      = norm(ray.pos - g1center)
            ray.v  = refraction_vector(n_glass, n_air, ray.v, n)
            medium = "air_out"
            continue

        # image plane
        if ray.pos.x >= 12:
            print(f"incidence {angle:2d}/40 rad, y = {ray.pos.y:.5f} cm")
            break