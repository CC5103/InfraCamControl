import pigpio
import time

# GPIOピンの設定
GPIO_PIN = 14
pi = pigpio.pi()

# NEC赤外線信号のパルス時間設定 (マイクロ秒)
LEADER_PULSE_MIN = 8500
LEADER_PULSE_MAX = 9500
ZERO_PULSE_MIN = 500
ZERO_PULSE_MAX = 700
ONE_PULSE_MIN = 1500
ONE_PULSE_MAX = 1800

# 三菱赤外線信号のパルス時間設定 (マイクロ秒)
# LEADER_PULSE_MIN = 3000
# LEADER_PULSE_MAX = 3500
# ZERO_PULSE_MIN = 300
# ZERO_PULSE_MAX = 700
# ONE_PULSE_MIN = 1000
# ONE_PULSE_MAX = 1500 

# pigpio接続確認
if not pi.connected:
    print("Error: pigpioデーモンに接続できません。")
    exit()

# GPIO14を入力モードに設定
pi.set_mode(GPIO_PIN, pigpio.INPUT)

# 信号パルスのリスト
pulse_list = []
limit = 0
last_tick = pi.get_current_tick()
is_data_ready = False  # データの準備完了フラグ

# コールバック関数: 赤外線信号を処理
def pulse_callback(gpio, level, tick):
    """
    赤外線信号のパルスを処理するコールバック関数。
    """
    global last_tick, is_data_ready, limit
    pulse_duration = tick - last_tick

    if limit <= 1:
        if LEADER_PULSE_MIN <= pulse_duration <= LEADER_PULSE_MAX:
            limit += 1
            print("Leader pulse detected.")
        elif level == 0:
            if ZERO_PULSE_MIN <= pulse_duration <= ZERO_PULSE_MAX:
                pulse_list.append(0)
                print("Zero pulse detected.")
            elif ONE_PULSE_MIN <= pulse_duration <= ONE_PULSE_MAX:
                pulse_list.append(1)
                print("One pulse detected.")
            else:
                print("Invalid pulse detected.")
        last_tick = tick
        if limit > 1:
            is_data_ready = True

# GPIO14にコールバック設定
pi.callback(GPIO_PIN, pigpio.EITHER_EDGE, pulse_callback)

try:
    print("Listening for IR signals...")
    while True:
        time.sleep(1)  # プログラムを保持し、信号を待機
        if is_data_ready:
            # データを保存
            with open("data3.csv", "w") as f:
                f.write(" ".join(map(str, pulse_list)))
            print(f"Data saved. Length: {len(pulse_list)}")
            break
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    pi.stop()  # pigpioの終了
    print("Cleanup completed.")