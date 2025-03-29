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
scene = canvas(title="懸鏈線波動模擬", width=800, height=400, center=vector(0, -5, 0), background=color.white)

# 初始節點位置與速度
balls = []
springs = []
positions = [vector(i * length / (n - 1) - length / 2, -5, 20) for i in range(n)]
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
balls[n // 2].pos.y += 2  # 中間的球向上位移

# 模擬主循環
while True:
    rate(1000)
    forces = [vector(0, -m * g, 0) for _ in range(n)]  # 重力作用

    # 計算彈簧作用力
    for i in range(1, n):
        spring_vector = balls[i].pos - balls[i - 1].pos
        stretch = mag(spring_vector) - length / (n - 1)
        force = -k * stretch * norm(spring_vector)
        forces[i] += force
        forces[i - 1] -= force

    # 更新位置和速度
    for i in range(n):
        if i not in fixed_points:  # 固定點不運動
            velocities[i] += (forces[i] / m - damping * velocities[i]) * dt
            balls[i].pos += velocities[i] * dt

    # 更新彈簧
    for i in range(1, n):
        springs[i - 1].pos = balls[i - 1].pos
        springs[i - 1].axis = balls[i].pos - balls[i - 1].pos

