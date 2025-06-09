from vpython import *
import numpy as np

# ---------------------- 基本參數 ---------------------- #
N = 100                     # 網格數 (NxN)
R = 1.0                     # 球幕半徑 (m)
lam = 500e-9                # 波長 (m)
d = 100e-6                  # 孔徑直徑 (m)
k = 2 * np.pi / lam         # 波數
dx = dy = d / N             # 孔平面格點間距

# ---------------------- 建立孔平面格點 ---------------------- #
x_ap = np.linspace(-d/2 + dx/2, d/2 - dx/2, N)
y_ap = x_ap
X, Y = np.meshgrid(x_ap, y_ap)
mask = X**2 + Y**2 <= (d/2)**2          # 圓孔內部的格點才會發光
X_src, Y_src = X[mask], Y[mask]         # 發光點座標一維化
M = X_src.size                          # 發光點總數

# ---------------------- 觀測方向 (小角度近似) ---------------------- #
theta_side = np.linspace(-0.01*np.pi, 0.01*np.pi, N)
theta_x, theta_y = np.meshgrid(theta_side, theta_side)

# ---------------------- 計算電場振幅 ---------------------- #
# A(θx,θy) = Σ cos(k (θx X + θy Y))  (對稱性使 sin 項相消)
E_field = np.zeros_like(theta_x)
for X0, Y0 in zip(X_src, Y_src):
    phase = k * (theta_x * X0 + theta_y * Y0)
    E_field += np.cos(phase)
E_field /= M                                # (可省略常數，但歸一化較好看)

# ---------------------- 兩種強度影像 ---------------------- #
I_real  = E_field ** 2
I_false = np.abs(E_field)

# ---------------------- 找第一暗環半徑 ---------------------- #
# 取中心橫向剖面 (θy=0) 作為 1D 強度，往外尋第一次接近 0 的點
center_idx = N // 2
profile = I_real[center_idx, :]
peak = profile[center_idx]
thr  = 0.05 * peak                         # 5% 閾值
idx_dark = np.where(profile[center_idx+1:] < thr)[0][0] + (center_idx+1)
theta_step = theta_side[1] - theta_side[0]
theta_first = np.abs(theta_side[idx_dark]) # rad
r_first = R * theta_first                 # m

# ---------------------- 理論萊利判據 ---------------------- #
r_rayleigh = 1.22 * lam * R / d

print(f"第一暗環半徑 (模擬) = {r_first*1e3:.2f} mm")
print(f"Rayleigh 公式      = {r_rayleigh*1e3:.2f} mm")
print(f"是否滿足 Rayleigh？ {'Yes' if abs(r_first-r_rayleigh)/r_rayleigh < 0.1 else 'No'}")

# ---------------------- VPython 畫面 ---------------------- #
scene1 = canvas(align='left',  height=600, width=600,
                center=vector(N*dx/2, N*dy/2, 0),
                title="True intensity  |A|²")
scene2 = canvas(align='right', x=600, height=600, width=600,
                center=vector(N*dx/2, N*dy/2, 0),
                title="False intensity |A|")

for scene, data in ((scene1, I_real), (scene2, I_false)):
    scene.lights = []
    scene.ambient = color.gray(0.99)
    maxI = np.amax(data)
    for i in range(N):
        for j in range(N):
            gray = data[i, j] / maxI
            box(canvas=scene,
                pos=vector(i*dx, j*dy, 0),
                length=dx, height=dy, width=dx,
                color=vector(gray, gray, gray))