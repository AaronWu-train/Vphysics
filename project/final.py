from vpython import *

# === 參數設定 ===
L = 30  # 繪圖範圍的半長
size_big = 5  # 大方塊的邊長
size_small = 2  # 小方塊的邊長
mass_small = 1  # 小方塊的質量
v_big = -10  # 大方塊的初速度
v_small = 0  # 小方塊的初速度

# === 圖形視窗與繪圖設定 ===
# 主場景設定
scene = canvas(
    align="left",
    center=vec(0, 5, 0),
    height=800,
    width=800,
    background=vec(0.5, 0.5, 0),
)

# 碰撞次數與理論 π 值比較圖
collision_graph = graph(
    title="Collision Count vs. Mass Ratio",
    xtitle="log100(Mass Ratio)",
    ytitle="Collision Count / 10^i",
    width=600,
    height=400,
    background=color.white,
    align="right",
    ymin=2.97,
    ymax=3.21,
)
pi_curve = gcurve(graph=collision_graph, color=color.yellow, label="y = π")  # 理論 π 值
collision_curve = gcurve(graph=collision_graph, color=color.red, label="Collision Count / 10^i")  # 碰撞次數曲線

# 右上資訊面板
info_panel = label(
    pos=vec(0, 30, 0),
    text="",
    height=20,
    box=False,
    border=5,
    font="monospace",
    color=color.white,
)

# 地板與牆壁
floor = box(length=2 * L, height=0.01, width=size_big, color=color.blue, pos=vector(0, 0, 0))
wall = box(pos=vector(-L, size_big / 2, 0), size=vector(0.2, size_big, size_big), color=color.gray(0.5))

# 大方塊與小方塊
big_block = box(pos=vector(0, size_big / 2, 0), size=vector(size_big, size_big, size_big), color=color.blue)
small_block = box(pos=vector(-L / 2, size_small / 2, 0), size=vector(size_small, size_small, size_small), color=color.red)

# === 預設理論 π 曲線 ===
for i in range(6):
    pi_curve.plot(i, pi)

# === 主模擬迴圈 ===
for i in range(6):
    # 設定質量比
    mass_big = 100 ** i
    collision_count = 0

    # 初始速度
    v_big_vector = vector(v_big, 0, 0)
    v_small_vector = vector(v_small, 0, 0)

    # 重設方塊位置
    big_block.pos = vector(0, size_big / 2, 0)
    small_block.pos = vector(-L / 2, size_small / 2, 0)

    # 時間參數
    dt = min(max(0.001 * 10 ** (-i), 0.000001), 0.001)
    scene.autoscale = False  # 禁用自動縮放

    # 模擬進行
    while True:
        # 控制模擬速度
        if i >= 3:
            rate(100000 / dt)
        elif i == 2:
            rate(50 / dt)
        elif i == 1:
            rate(10000)
        else:
            rate(1000)

        # 更新位置
        big_block.pos += v_big_vector * dt
        small_block.pos += v_small_vector * dt

        # 更新右側資訊面板
        info_panel.text = (
            f"Mass Ratio: {mass_small} : {mass_big}\n"
            f"Collisions: {collision_count}\n"
            f"Big Block Velocity: {v_big_vector.x:.6f}\n"
            f"Small Block Velocity: {v_small_vector.x:.6f}"
        )

        # 小方塊與牆壁碰撞檢測
        if small_block.pos.x - size_small / 2 <= wall.pos.x + 0.1:
            v_small_vector.x = -v_small_vector.x
            collision_count += 1

        # 大方塊與小方塊碰撞檢測
        if small_block.pos.x + size_small / 2 >= big_block.pos.x - size_big / 2:
            v_big_new = ((mass_big - mass_small) * v_big_vector.x + 2 * mass_small * v_small_vector.x) / (mass_big + mass_small)
            v_small_new = ((mass_small - mass_big) * v_small_vector.x + 2 * mass_big * v_big_vector.x) / (mass_big + mass_small)
            v_big_vector.x = v_big_new
            v_small_vector.x = v_small_new
            collision_count += 1
        
        # 更新右側資訊面板
        info_panel.text = (
            f"Mass Ratio: {mass_small} : {mass_big}\n"
            f"Collisions: {collision_count}\n"
            f"Big Block Velocity: {v_big_vector.x:.6f}\n"
            f"Small Block Velocity: {v_small_vector.x:.6f}"
        )

        # 停止條件 (速度接近穩定)
        if (
            big_block.pos.x + size_big > L / 2
            and v_big_vector.x > 0
            and v_small_vector.x >= 0
            and v_small_vector.x < v_big_vector.x
        ):
            break

    # 輸出結果並繪圖
    # 更新右側資訊面板
    info_panel.text = (
        f"Mass Ratio: {mass_small} : {mass_big}\n"
        f"Collisions: {collision_count}\n"
        f"Big Block Velocity: {v_big_vector.x:.6f}\n"
        f"Small Block Velocity: {v_small_vector.x:.6f}"
    )
    print(f"Mass Ratio: {mass_small} : {mass_big}")
    print("Collisions / (10^i) =", collision_count)
    log_mass_ratio = i
    collision_curve.plot(log_mass_ratio, collision_count / (10 ** i))
    sleep(1)

sleep(1)
exit()
