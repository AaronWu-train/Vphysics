from vpython import *

# 參數設定
n = 50  # 懸鏈線上的節點數量
length = 100  # 懸鏈線初始總長度
g = 9.8  # 重力加速度
k = 100  # 彈簧常數
damping = 0.05  # 阻尼因子
m = 0.1  # 每個小球的質量
dt = 0.005  # 時間步長

# 創建場景
scene = canvas(title="阻尼懸鏈線波動模擬", width=800, height=400, center=vector(0, -5, 0), background=color.white, align='left')

# 創建圖表
energy_graph = graph(title="能量 vs 時間", xtitle="時間 (s)", ytitle="能量 (J)", width=600, height=400, align='right')
total_energy_curve = gcurve(graph=energy_graph, color=color.red, label="總能量")
kinetic_energy_curve = gcurve(graph=energy_graph, color=color.blue, label="總動能")
potential_energy_curve = gcurve(graph=energy_graph, color=color.green, label="總位能")

# 初始節點位置與速度
balls = []
springs = []
positions = [vector(i * length / (n - 1) - length / 2, 20, 0) for i in range(n)]
velocities = [vector(0, 0, 0) for _ in range(n)]

# 固定第一個與最後一個節點
fixed_points = [0, n - 1]

# 創建小球與彈簧
for i in range(n):
    ball = sphere(pos=positions[i], radius=0.4, color=color.red if i in fixed_points else color.blue, make_trail=False)
    balls.append(ball)
    if i > 0:
        spring = cylinder(pos=balls[i - 1].pos, axis=balls[i].pos - balls[i - 1].pos, radius=0.05, color=color.gray(0.5))
        springs.append(spring)

# 添加初始位移作為波動源
balls[n//2].pos.y += 3 # 中間的球向上位移

# 模擬主循環
t = 0
natural_length = length / (n - 1)  # 每段彈簧的自然長度
while True:
    rate(1000)
    forces = [vector(0, -m * g, 0) for _ in range(n)]  # 重力作用

    # 計算彈簧作用力
    total_spring_potential_energy = 0
    for i in range(1, n):
        spring_vector = balls[i].pos - balls[i - 1].pos
        stretch = mag(spring_vector) - natural_length
        force = -k * stretch * norm(spring_vector)
        forces[i] += force
        forces[i - 1] -= force
        # 計算彈簧的彈力位能
        total_spring_potential_energy += 0.5 * k * (stretch ** 2)

    # 更新位置和速度
    total_kinetic_energy = 0
    gravitational_potential_energy = 0
    for i in range(n):
        if i not in fixed_points:  # 固定點不運動
            velocities[i] += (forces[i] / m - damping * velocities[i]) * dt
            balls[i].pos += velocities[i] * dt
            total_kinetic_energy += 0.5 * m * mag(velocities[i]) ** 2
            gravitational_potential_energy += m * g * (balls[i].pos.y - 20)  # 位能相對基準面

    # 更新彈簧
    for i in range(1, n):
        springs[i - 1].pos = balls[i - 1].pos
        springs[i - 1].axis = balls[i].pos - balls[i - 1].pos

    # 計算總能量
    total_potential_energy = gravitational_potential_energy + total_spring_potential_energy
    total_energy = total_kinetic_energy + total_potential_energy

    # 繪製能量圖表
    total_energy_curve.plot(t, total_energy)
    kinetic_energy_curve.plot(t, total_kinetic_energy)
    potential_energy_curve.plot(t, total_potential_energy)

    # 更新時間
    t += dt

