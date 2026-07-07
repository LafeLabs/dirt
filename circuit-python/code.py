import time
import board
import math
import adafruit_lsm6ds.lsm6ds3trc

i2c = board.I2C()
sensor = adafruit_lsm6ds.lsm6ds3trc.LSM6DS3TRC(i2c)

# Initialize filtered values with the first reading
f_x, f_y, f_z = sensor.acceleration

# Precise smoothing factor for a 20Hz filter at your 0.05s loop rate
ALPHA = 0.84

while True:
    # 1. Read raw acceleration values instantly
    g_x, g_y, g_z = sensor.acceleration

    # 2. Apply the 20 Hz low-pass filter
    f_x = (ALPHA * f_x) + ((1 - ALPHA) * g_x)
    f_y = (ALPHA * f_y) + ((1 - ALPHA) * g_y)
    f_z = (ALPHA * f_z) + ((1 - ALPHA) * g_z)

    # 3. Format cleanly for the plotter to show three separate lines
    print(f"({f_x:.2f}, {f_y:.2f}, {f_z:.2f})")

    # Your perfect rate
    time.sleep(0.05)
