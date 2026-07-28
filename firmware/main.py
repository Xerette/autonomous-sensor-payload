from machine import Pin, I2C, SPI
import time
import os
import math
from bme280 import BME280
from micropython_bmi270 import bmi270
import sdcard
from ssd1306 import SSD1306_I2C

# ---------------------------------------------------------------------------
# I2C bus - BME280 + BMI270 + OLED (shared bus, chained via Qwiic)
# ---------------------------------------------------------------------------
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
bme = BME280(i2c=i2c, address=0x77)
bmi = bmi270.BMI270(i2c)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3d)

# ---------------------------------------------------------------------------
# SPI bus - microSD
# ---------------------------------------------------------------------------
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
cs = Pin(5)
sd = sdcard.SDCard(spi, cs)
os.mount(sd, '/sd')

# ---------------------------------------------------------------------------
# Session bookkeeping: a tiny counter file on the SD card tracks how many
# times the payload has booted. No RTC, no WiFi - fully standalone. Each
# session gets its own log file, so runs are never mixed together.
# ---------------------------------------------------------------------------
SESSION_COUNTER_PATH = '/sd/session_count.txt'
LOG_DIR = '/sd/logs'

try:
    with open(SESSION_COUNTER_PATH) as f:
        session_num = int(f.read().strip())
except (OSError, ValueError):
    session_num = 0

session_num += 1

with open(SESSION_COUNTER_PATH, 'w') as f:
    f.write(str(session_num))

try:
    os.mkdir(LOG_DIR)
except OSError:
    pass  # directory already exists - fine

LOG_PATH = '{}/session_{:04d}.csv'.format(LOG_DIR, session_num)

with open(LOG_PATH, 'w') as f:
    f.write(
        "time_s,temperature_C,pressure_Pa,humidity_percent,"
        "accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,roll_deg,pitch_deg\n"
    )

# ---------------------------------------------------------------------------
# OLED drawing helpers
# ---------------------------------------------------------------------------
OLED_W, OLED_H = 128, 64

# scrolling graph region: roll angle history
GRAPH_X, GRAPH_Y = 0, 10
GRAPH_W, GRAPH_H = 128, 24
graph_buf = [GRAPH_H // 2] * GRAPH_W  # start flat at the zero-reference line

# bubble-level region: live orientation dot
LEVEL_CX, LEVEL_CY = 64, 49
LEVEL_R = 13


def draw_circle(fb, cx, cy, r, color=1):
    """Midpoint circle algorithm - draws a circle outline pixel by pixel."""
    x, y, err = r, 0, 0
    while x >= y:
        fb.pixel(cx + x, cy + y, color)
        fb.pixel(cx + y, cy + x, color)
        fb.pixel(cx - y, cy + x, color)
        fb.pixel(cx - x, cy + y, color)
        fb.pixel(cx - x, cy - y, color)
        fb.pixel(cx - y, cy - x, color)
        fb.pixel(cx + y, cy - x, color)
        fb.pixel(cx + x, cy - y, color)
        y += 1
        if err <= 0:
            err += 2 * y + 1
        if err > 0:
            x -= 1
            err -= 2 * x + 1


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def draw_frame(session_num, sample_count, roll_deg, pitch_deg):
    oled.fill(0)

    # header: which session, how many samples logged so far this session
    oled.text("S{:04d} n={}".format(session_num, sample_count), 0, 0)

    # dashed zero-reference line through the middle of the graph
    ref_y = GRAPH_Y + GRAPH_H // 2
    for x in range(0, OLED_W, 4):
        oled.pixel(x, ref_y, 1)

    # scrolling graph: shift buffer left, plot new roll sample on the right
    clamped_roll = clamp(roll_deg, -90, 90)
    y_offset = (GRAPH_H - 1) - int(((clamped_roll + 90) / 180) * (GRAPH_H - 1))
    graph_buf.pop(0)
    graph_buf.append(y_offset)
    for x in range(GRAPH_W - 1):
        oled.line(
            GRAPH_X + x, GRAPH_Y + graph_buf[x],
            GRAPH_X + x + 1, GRAPH_Y + graph_buf[x + 1],
            1
        )

    # bubble-level: circle boundary + a dot showing current tilt direction
    draw_circle(oled, LEVEL_CX, LEVEL_CY, LEVEL_R, 1)
    dot_x = LEVEL_CX + int(clamp(pitch_deg, -90, 90) / 90 * (LEVEL_R - 3))
    dot_y = LEVEL_CY + int(clamp(roll_deg, -90, 90) / 90 * (LEVEL_R - 3))
    oled.fill_rect(dot_x - 1, dot_y - 1, 3, 3, 1)

    oled.show()


# ---------------------------------------------------------------------------
# Startup splash - makes the session boundary visible on the OLED, not just
# in the filename
# ---------------------------------------------------------------------------
oled.fill(0)
oled.text("Session {:04d}".format(session_num), 0, 24)
oled.text("starting...", 0, 36)
oled.show()
time.sleep(1.5)

# ---------------------------------------------------------------------------
# Main loop - read both sensors, log to this session's file, update OLED
# ---------------------------------------------------------------------------
start_time = time.time()
sample_count = 0

while True:
    current_time = time.time() - start_time

    temperature_C, pressure_Pa, humidity_percent = bme.read_compensated_data()
    accx, accy, accz = bmi.acceleration
    gyrox, gyroy, gyroz = bmi.gyro

    pitch_deg = math.degrees(math.atan2(-accx, math.sqrt(accy * accy + accz * accz)))
    roll_deg = math.degrees(math.atan2(accy, accz))

    line = "{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}".format(
        current_time,
        temperature_C, pressure_Pa, humidity_percent,
        accx, accy, accz,
        gyrox, gyroy, gyroz,
        roll_deg, pitch_deg
    )
    print(line)  # only visible if a computer happens to be connected - harmless otherwise

    with open(LOG_PATH, 'a') as f:
        f.write(line + "\n")

    sample_count += 1
    draw_frame(session_num, sample_count, roll_deg, pitch_deg)

    time.sleep(1)