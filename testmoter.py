# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 18:02:32 2020

@author: Souichirou Kikuchi
"""

import spidev
import RPi.GPIO as GPIO
from time import sleep

CHN = 0 # ADコンバーター接続チャンネル
MOTOR_PWM0 = 25 # DC Motor PWM0
MOTOR_PWM1 = 24 # DC Motor PWM1

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PWM0, GPIO.OUT)
GPIO.setup(MOTOR_PWM1, GPIO.OUT)
pwm0 = GPIO.PWM(MOTOR_PWM0, 50)  # 周波数50Hz
pwm1 = GPIO.PWM(MOTOR_PWM1, 50)  # 周波数50Hz
pwm0.start(0)
pwm1.start(0)

spi = spidev.SpiDev()
spi.open(0, 0) # 0：SPI0、0：CE0
spi.max_speed_hz = 1000000 # 1MHz SPIのバージョンアップによりこの指定をしないと動かない

def get_data(channel):
    dout = spi.xfer2([((0b1000+channel)>>2)+0b100,((0b1000+channel)&0b0011)<<6,0]) # Din(RasPi→MCP3208）を指定
    bit12 = ((dout[1]&0b1111) << 8) + dout[2] # Dout（MCP3208→RasPi）から12ビットを取り出す
    return float(bit12) # 通常なら0～4095だが両端に330Ωの抵抗を入れているので120～3975程度の範囲になる

try:
    print('--- start program ---')
    while True:
        val = get_data(CHN)
        print('val= ',val)
        if val > 100 and val < 2048:
            pwm1.ChangeDutyCycle(0)
            duty = (2048 - val) * 50 / 2048
            pwm0.ChangeDutyCycle(duty)
        elif val >= 2048 and val < 4000:
            pwm0.ChangeDutyCycle(0)
            duty = (val - 2048) * 50 / 2048
            pwm1.ChangeDutyCycle(duty)
        sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    pwm0.stop()
    pwm1.stop()
    spi.close()
    GPIO.cleanup()
    print('--- stop program ---')
