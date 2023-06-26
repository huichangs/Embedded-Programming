import smbus
import math
import RPi.GPIO as gpio
import time
import numpy as np
import cv2
import RPi.GPIO as gpio
import time
# Cascades 디렉토리의 haarcascade_frontalface_default.xml 파일을 Classifier로 사용
faceCascade = cv2.CascadeClassifier('/home/huichang/.local/lib/python3.9/site-packages/cv2/data/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

pwr_mgmt_1 = 0x6B
gyro_xout_addr = 0x43
gyro_yout_addr = 0x45
gyro_zout_addr = 0x47

bus = smbus.SMBus(1)
address = 0x68

def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    high = bus.read_byte_data(address, reg)
    low = bus.read_byte_data(address, reg + 1)
    value = (high << 8) + low
    return value

def read_word_2c(reg):
    value = read_word(reg)
    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value
        
def dist(a,b):
    return math.sqrt((a * a) + (b * b))
    
def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)

def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)
        
def MPU6050_init():
    bus.write_byte_data(address, pwr_mgmt_1, 1)
    
def angle_to_pulse_width(angle):
    pulse_width = (angle / 180) *(2.5 - 0.5) + 0.5
    return pulse_width

is_pin_on = 0
pwm_pin1 = 12
pwm_pin2 = 16
pwm_pin3 = 20

gpio.setmode(gpio.BCM)
gpio.setup(pwm_pin1, gpio.OUT)
gpio.setup(pwm_pin2, gpio.OUT)
gpio.setup(pwm_pin3, gpio.OUT)

servo1 = gpio.PWM(pwm_pin1, 50)
servo2 = gpio.PWM(pwm_pin2, 50)
servo3 = gpio.PWM(pwm_pin3, 50)

servo1.start(0)
servo2.start(0)
servo3.start(0)

angle1 = 8.8
angle2 = 5.5
angle3 = 11

try:
    MPU6050_init()
    
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(20, 20)
        )
        
        face_rotation_z = 0
        face_rotation_y = 0
        #만약 얼굴이 인식된다면 rotation_z값 바꿈
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            face_rotation_z = 320 - (x + w/2)
            face_rotation_y = 240 - (y + h/2)
            
        #얼굴인식이 안되었다면 rotation_z값은 0, 되었다면 rotation_z값
        angle1 = round(angle1 - face_rotation_z / 320, 1)
        if(angle1 < 2.5):
            angle1 = 2.5
        elif(angle1 > 12.5):
            angle1 = 12.5
        #print(angle1)
        cv2.imshow('video',img)
        
        
        gyro_xout = read_word_2c(gyro_xout_addr)
        gyro_yout = read_word_2c(gyro_yout_addr)
        gyro_zout = read_word_2c(gyro_zout_addr)
        
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)
        
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        
        x_rotation = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        y_rotation = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        
        #y축회전. 얼굴인식이 되었다면 face_rotation_y반영
        angle2 = round(angle2 + y_rotation / 180 + face_rotation_y / 350, 1)
        if(angle2 < 2.5):
            angle2 = 2.5
        elif(angle2 > 12.5):
            angle2 = 12.5
        #print(angle2)
        
        #x축회전.
        angle3 = round(angle3 - x_rotation / 180, 1)
        if(angle3 < 2.5):
            angle3 = 2.5
        elif(angle3 > 12.5):
            angle3 = 12.5
        #print(angle3)
        
        servo1.ChangeDutyCycle(angle1)
        #servo2.ChangeDutyCycle(angle2)
        #servo3.ChangeDutyCycle(angle3)
        
        time.sleep(0.05)
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit # ESC를 누르면 종료
            break
            
    servo1.stop()
    servo2.stop()
    servo3.stop()
    gpio.cleanup()
    cap.release()
    cv2.destroyAllWindows()
        
        
except KeyboardInterrupt:
    servo1.stop()
    servo2.stop()
    servo3.stop()
    gpio.cleanup()

