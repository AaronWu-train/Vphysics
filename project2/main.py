import vpython as vp
import numpy as np

# 設定場景
scene = vp.canvas(title='電子在平行金屬板中的運動軌跡',
                  width=1200, height=600,
                  background=vp.color.black)

# 物理常數
q = -1.6e-19          # 電子電荷量 (C)
m = 9.1e-31           # 電子質量 (kg)

# 平行板參數
plate_length = 0.1    # 平板長度 (m)
plate_width  = 0.02   # 平板寬度 (m)
plate_separation = 0.1
voltage = 500         # 電壓 (V)

# 電、磁場
E = voltage / plate_separation
E_vec = vp.vector(0, -E, 0)
B_strength = 5e-4   # 0.25 mT，向 -z
B_vec = vp.vector(0, 0, -B_strength)

# 上下平行板
upper = vp.box(pos=vp.vector(plate_length/2,  plate_separation/2, 0),
               size=vp.vector(plate_length, 0.002, plate_width),
               color=vp.color.red)
lower = vp.box(pos=vp.vector(plate_length/2, -plate_separation/2, 0),
               size=vp.vector(plate_length, 0.002, plate_width),
               color=vp.color.blue)
vp.label(pos=upper.pos + vp.vector(0, 0.005, 0), text='正極板 (+)', color=vp.color.red)
vp.label(pos=lower.pos + vp.vector(0,-0.005, 0), text='負極板 (-)', color=vp.color.blue)

# ── 1. 多顆粒子的初速與顏色 ─────────────────────────── #
speeds  = [5.0e6, 7e6, 1.0e7, 2.0e7, 4e7, 8e7]   # m/s
colors  = [vp.color.red, vp.color.orange, vp.color.yellow,
           vp.color.green, vp.color.cyan, vp.color.blue]

particles = []   # 每顆粒子用 dict 存狀態
for v0, col in zip(speeds, colors):
    sphere = vp.sphere(pos=vp.vector(0, 0, 0),
                       radius=0.001,
                       color=col,
                       make_trail=True,
                       trail_color=col,
                       trail_radius=0.00033)
    particles.append({
        "obj": sphere,
        "v": vp.vector(v0, 0, 0),  # 初速沿 +x
        "active": True,
        "color": col
    })

# 介面資訊
vp.wtext(text=f"電壓: {voltage} V\n電場: {E:.2e} V/m\n"
              f"磁場: {B_strength:.2e} T (-z)\n"
              f"初速: {', '.join(f'{v:.1e}' for v in speeds)} m/s\n")

dt = 5e-13
t  = 0

print("模擬開始…")

# ── 3. 主迴圈：同時更新所有粒子 ─────────────────────── #
while True:
    vp.rate(1000)
    active_count = 0

    for p in particles:
        if not p["active"]:
            continue

        # 計算洛侖茲力與加速度
        v_vec = p["v"]
        F_vec = q * (E_vec + vp.cross(v_vec, B_vec))
        a_vec = F_vec / m

        # 更新速度與位置
        p["v"] += a_vec * dt
        p["obj"].pos += p["v"] * dt

        # 判斷是否離開或撞板
        x, y = p["obj"].pos.x, p["obj"].pos.y
        if x > plate_length or abs(y) > plate_separation/2:
            tag = "離開平板" if x > plate_length else "撞到平板"
            print(f"\n[{tag}]  初速 {abs(p['v'].x):.2e} m/s  "
                  f"終點 (x={x:.4f}, y={y:.4f})  飛行時間 {t:.2e}s")
            # 標記終點
            vp.sphere(pos=p["obj"].pos, radius=0.002,
                      color=p["color"], opacity=0.5)
            p["active"] = False
        else:
            active_count += 1

    if active_count == 0:
        print("\n全部粒子完結，模擬結束！")
        break

    t += dt
