from vpython import *

# 參數設定
L = 30 
size_big = 5 # 大方塊的邊長
size_small = 1  # 小方塊的邊長
#mass_big = 100  # 大方塊的質量
mass_small = 1  # 小方塊的質量
v_big = -10  # 大方塊的初速度
v_small = 0  # 小方塊的初速度

# 碰撞計數器

# 牆、大方塊、小方塊
scene = canvas(
    align="left",
    center=vec(0, 5, 0),
    height=800,
    width=800,
    background=vec(0.5, 0.5, 0),
)
floor = box(length=2*L, height=0.01, width=size_big, color=color.blue, pos=vector(0, 0, 0))
wall = box(pos=vector(-L, size_big/2, 0), size=vector(0.2, size_big, size_big), color=color.gray(0.5))
big_block = box(pos=vector(0, size_big/2, 0), size=vector(size_big, size_big, size_big), color=color.blue)
small_block = box(pos=vector(-L/2, size_small/2, 0), size=vector(size_small, size_small, size_small), color=color.red)

for i in range(6):
    mass_big = 100 ** i
    collision_count = 0
    v_big_vector = vector(v_big, 0, 0)
    v_small_vector = vector(v_small, 0, 0)
    big_block.pos = vector(0, size_big/2, 0)
    small_block.pos = vector(-L/2, size_small/2, 0)

    # 時間參數
    dt = 0.000001

    # 模擬
    while True:
        rate(1000000)  # 控制模擬速度

        # 更新位置
        big_block.pos += v_big_vector * dt
        small_block.pos += v_small_vector * dt

        # 檢測小方塊與牆碰撞
        if small_block.pos.x - size_small / 2 <= wall.pos.x + 0.1:
            v_small_vector.x = -v_small_vector.x  # 速度反向
            collision_count += 1

        # 檢測大方塊與小方塊碰撞
        if small_block.pos.x + size_small / 2 >= big_block.pos.x - size_big / 2:
            # 碰撞公式
            v_big_new = ((mass_big - mass_small) * v_big_vector.x + 2 * mass_small * v_small_vector.x) / (mass_big + mass_small)
            v_small_new = ((mass_small - mass_big) * v_small_vector.x + 2 * mass_big * v_big_vector.x) / (mass_big + mass_small)
            
            v_big_vector.x = v_big_new
            v_small_vector.x = v_small_new
            
            collision_count += 1

        # 停止條件 (小方塊速度幾乎停止)
        if big_block.pos.x + size_big/2 > L and v_big_vector.x > 0  and v_small_vector.x < v_big_vector.x:
            break

    # 結果輸出
    print("Mass Ratio =", mass_big, ":" , mass_small)
    print("碰撞次數 =", collision_count)
    sleep(1)  # 等待一秒

exit()
