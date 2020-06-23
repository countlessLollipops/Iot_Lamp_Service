import serial
import time
import os

from django.shortcuts import render
from monitoring.models import OperationRecord

ser = serial.Serial('com2', 9600, timeout=10)
turnon_LED = bytes.fromhex('00')
turnoff_LED = bytes.fromhex('FF')
print('初始化串口完毕')
LED_status = 0

def get_status(request):
    global LED_status
    LED_status = get_LED_status()
    print(LED_status)
    return render(request, "monitoring.html", {'LED_status': LED_status})


def control(request):
    global LED_status

    if LED_status == 0:
        ser.write(turnon_LED)
        LED_status = 1
    elif LED_status == 1:
        ser.write(turnoff_LED)
        LED_status = 0

    # log_db(LED_status)

    light = get_brightness()
    print(type(light))
    time.sleep(1)
    temperature = get_temperature()
    brightness = monitor_brightness_control(light)

    return render(request, "monitoring.html", {'LED_status': LED_status,
                                               'current_brightness': brightness,
                                               'current_temperature': temperature,
                                               })


def get_LED_status():
    ser.write(bytes.fromhex('33'))
    if ser.inWaiting():
        data = ser.read(ser.inWaiting()).hex()
        print('灯的初始状态'+data)
        if data:
            return 0
        else:
            return 1


def log_db(LED_status):
    query = OperationRecord(name='开光灯', time='', value=LED_status)
    query.save()


def get_brightness():
    ser.write(bytes.fromhex('22'))
    if ser.inWaiting():
        data = ser.read(ser.inWaiting()).hex()
        data = int(data, 16)
        data = data * 5.0 / 256.0
        print('当前环境亮度：'+str(data))
        return data


def get_temperature():
    ser.write(bytes.fromhex('11'))
    if ser.inWaiting():
        data = ser.read(ser.inWaiting()).hex()
        data = int(data, 16)
        print('当前环境温度：'+str(data))
        return data


def monitor_brightness_control(brightness):
    print(type(brightness))
    if 0 <= brightness <= 0.92:  # <50lux
        data = 0
    elif 0.92 < brightness <= 1.45:  # 50~100lux
        data = 5
    elif 1.45 < brightness <= 1.83:  # 100~150lux
        data = 10
    elif 1.83 < brightness <= 2.13:  # 150~200lux
        data = 15
    elif 2.13 < brightness <= 2.36:  # 200~250lux
        data = 20
    elif 2.36 < brightness <= 2.56:  # 250~300lux
        data = 25
    elif 2.56 < brightness <= 2.72:  # 300~350lux
        data = 30
    elif 2.72 < brightness <= 2.87:  # 350~400lux
        data = 35
    elif 2.87 < brightness <= 2.99:  # 400~450lux
        data = 40
    elif 2.99 < brightness <= 3.1:  # 450~500lux
        data = 45
    elif 3.1 < brightness <= 3.19:  # 500~550lux
        data = 50
    elif 3.19 < brightness <= 3.28:  # 550~600lux
        data = 55
    elif 3.19 < brightness <= 3.28:  # 600~650lux
        data = 60
    elif 3.28 < brightness <= 3.35:  # 650~700lux
        data = 65
    elif 3.35 < brightness <= 3.42:  # 700~750lux
        data = 70
    elif 3.42 < brightness <= 3.49:  # 750~800lux
        data = 75
    elif 3.49 < brightness <= 3.54:  # 800~850lux
        data = 80
    elif 3.54 < brightness <= 3.6:  # 850~900lux
        data = 85
    elif 3.6 < brightness <= 3.65:  # 900~950lux
        data = 90
    elif 3.65 < brightness <= 3.69:  # 950~1000lux
        data = 95
    elif brightness > 3.69:  # 1000~lux
        data = 100
    else:
        data = 0

    cmd = 'ddm.exe /SetBrightnessLevel ' + str(data)
    os.system(cmd)
    return data
