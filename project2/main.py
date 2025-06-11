import vpython as vp
import numpy as np

# 設定場景
scene = vp.canvas(title='電子在平行金屬板中的運動軌跡', 
                  width=1200, height=600, 
                  background=vp.color.black)

# 物理常數
q = -1.6e-19  # 電子電荷量 (C)
m = 9.1e-31  # 電子質量 (kg)

# 平行板參數
plate_length = 0.1      # 平板長度 (m)
plate_width = 0.02      # 平板寬度 (m)
plate_separation = 0.1  # 平板間距 (m)
voltage = 500           # 電壓 (V)

# 計算電場強度
E = voltage / plate_separation  # 電場強度 (V/m)

# ============== 這裡開始：定義電場、磁場向量與電荷 ==============
E_vec = vp.vector(0, -E, 0)     # 與原來效果相同：受力仍向 +y
B_strength = 2.5e-4             # 垂直入紙面 (+z) 2 mT
B_vec = vp.vector(0, 0, -B_strength)
# ============================================================

# 創建上下平行板
upper_plate = vp.box(pos=vp.vector(plate_length/2, plate_separation/2, 0),
                     size=vp.vector(plate_length, 0.002, plate_width),
                     color=vp.color.red)

lower_plate = vp.box(pos=vp.vector(plate_length/2, -plate_separation/2, 0),
                     size=vp.vector(plate_length, 0.002, plate_width),
                     color=vp.color.blue)

# 添加標籤
upper_label = vp.label(pos=upper_plate.pos + vp.vector(0, 0.005, 0),
                       text='正極板 (+)', color=vp.color.red, height=12)
lower_label = vp.label(pos=lower_plate.pos + vp.vector(0, -0.005, 0),
                       text='負極板 (-)', color=vp.color.blue, height=12)

# 電子初始條件
electron_radius = 0.001
initial_x = 0
initial_y = 0  # 從平板中央開始
initial_z = 0

# 初始速度 (水平方向，比較快的速度)
v0 = 2e7  # m/s (約為光速的6.7%)
vx = v0
vy = 0
vz = 0

# 創建電子
electron = vp.sphere(pos=vp.vector(initial_x, initial_y, initial_z),
                     radius=electron_radius,
                     color=vp.color.yellow,
                     make_trail=True,
                     trail_color=vp.color.yellow,
                     trail_radius=electron_radius/3)

# 時間參數
dt = 1e-12  # 時間步長 (s)
t = 0

# 介面資訊
info_text = vp.wtext(text=f"電壓: {voltage} V\n"
                          f"電場強度: {E:.2e} V/m\n"
                          f"磁場強度: {B_strength:.2e} T (+z)\n"
                          f"初始速度: {v0:.2e} m/s\n")

print(f"模擬參數:")
print(f"平板長度: {plate_length} m")
print(f"平板間距: {plate_separation} m")
print(f"電壓: {voltage} V")
print(f"電場強度: {E:.2e} V/m")
print(f"電子初始速度: {v0:.2e} m/s")
print(f"預期飛行時間: {plate_length/v0:.2e} s")

# 運動模擬
while True:
    vp.rate(1000)  # 控制動畫速度

    # ---------- 洛侖茲力與加速度 ----------
    v_vec = vp.vector(vx, vy, vz)
    F_vec = q * (E_vec + vp.cross(v_vec, B_vec))
    a_vec = F_vec / m
    # -------------------------------------

    # 更新速度
    vx += a_vec.x * dt
    vy += a_vec.y * dt
    vz += a_vec.z * dt

    # 更新位置
    electron.pos.x += vx * dt
    electron.pos.y += vy * dt
    electron.pos.z += vz * dt

    # 更新時間
    t += dt

    # 檢查是否離開平板區域
    if electron.pos.x > plate_length:
        print(f"\n電子離開平板區域!")
        print(f"飛行時間: {t:.2e} s")
        print(f"最終位置: x={electron.pos.x:.4f} m, y={electron.pos.y:.4f} m")
        print(f"最終速度: vx={vx:.2e} m/s, vy={vy:.2e} m/s, vz={vz:.2e} m/s")
        print(f"偏轉角度 (xy): {np.degrees(np.arctan2(vy, vx)):.2f}°")
        break

    # 檢查是否撞到平板
    if abs(electron.pos.y) > plate_separation/2:
        print(f"\n電子撞到平板!")
        print(f"撞擊時間: {t:.2e} s")
        print(f"撞擊位置: x={electron.pos.x:.4f} m, y={electron.pos.y:.4f} m")
        break

# 添加最終軌跡標記
final_marker = vp.sphere(pos=electron.pos,
                         radius=electron_radius*2,
                         color=vp.color.green,
                         opacity=0.5)

final_label = vp.label(pos=electron.pos + vp.vector(0, 0.003, 0),
                       text=f'結束位置\n({electron.pos.x:.3f}, {electron.pos.y:.3f})',
                       color=vp.color.green, height=10)

print("\n模擬完成!")
print("軌跡說明: 黃色軌跡線顯示電子的運動路徑，現同時受電場與垂直磁場影響。")
