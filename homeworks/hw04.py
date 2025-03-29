import numpy as np
from vpython import *

# 定義系統參數
A, N = 0.10, 50
m, k, d = 0.1, 10.0, 0.4


# 定義一個空類來模擬粒子
class Particle:
    pass


particles = [Particle() for i in range(N)]
connectors = [Particle() for i in range(N - 1)]

# 初始化時間參數
time, time_step = 0, 0.0003

# 設定繪圖參數
graph_view = graph(
    width=1000,
    height=500,
    align="left",
    xtitle="Wave Vector (k)",
    ytitle="Angular Frequency (ω)",
)
frequency_curve = gcurve(graph=graph_view, color=color.red, width=3)

# 探索不同波向量模式
for mode_index in arange(1, N / 2 - 1, 1.0):
    wave_unit = 2 * np.pi / (N * d)
    wave_vector = mode_index * wave_unit
    initial_phase = wave_vector * np.arange(N) * d

    # 初始化粒子狀態
    ball_pos = np.arange(N) * d + A * np.sin(initial_phase)
    ball_orig = np.arange(N) * d
    velocities = np.zeros(N)
    spring_len = np.ones(N) * d

    wave_count = 0
    time = 0

    # 開始模擬
    while wave_count < 10:
        time += time_step
        spring_len[:-1] = ball_pos[1:] - ball_pos[:-1]
        velocities[1:] += (spring_len[1:] - spring_len[:-1]) * k / m * time_step

        # 週期性邊界條件處理
        spring_len[-1] = ball_pos[0] - ball_pos[-1] + N * d
        velocities[0] += (spring_len[0] - spring_len[-1]) * k / m * time_step

        # 計算波動次數
        if (
            ball_pos[0] * (ball_pos[0] + velocities[0] * time_step) < 0
            and time > 5 * time_step
        ):
            wave_count += 0.5

        # 更新粒子位置
        ball_pos += velocities * time_step

    # 計算平均週期與繪圖
    average_period = time / wave_count
    frequency_curve.plot(wave_vector, 2.0 * np.pi / average_period)
