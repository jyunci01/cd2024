# pip install pyzmq cbor keyboard
from zmqRemoteApi import RemoteAPIClient
from zmqRemoteApi_IPv6 import RemoteAPIClient
import keyboard
import random
import math
import time

client = RemoteAPIClient('localhost', 23000)
# client = RemoteAPIClient('2001:288:6004:17:2023:cda:4:6', 23000)

print('Program started')
sim = client.getObject('sim')
sim.startSimulation()  # 確保模擬已經啟動
print('Simulation started')

v = 8
z = 40

# 選擇控制的球員
player = '/1_1'

def setVelocity(lfwV, rfwV, lbwV, rbwV):
    leftMotor1 = sim.getObject(player + '/joint_fr')  # 交換左前和右前
    rightMotor1 = sim.getObject(player + '/joint_fl')  # 交換左前和右前
    leftMotor2 = sim.getObject(player + '/joint_br')  # 交換左後和右後
    rightMotor2 = sim.getObject(player + '/joint_bl')  # 交換左後和右後
    sim.setJointTargetVelocity(leftMotor1, lfwV)
    sim.setJointTargetVelocity(rightMotor1, rfwV)
    sim.setJointTargetVelocity(leftMotor2, lbwV)
    sim.setJointTargetVelocity(rightMotor2, rbwV)
    # 輸入四個變數分別給四個軸速度

def setAngle(z):
    ontology = sim.getObject(player)
    angle = [-90 * math.pi / 180, 0 * math.pi / 180, z * math.pi / 180]
    leftMotor = sim.getObject(player + '/joint_fr')  # 交換左前和右前
    rightMotor = sim.getObject(player + '/joint_fl')  # 交換左前和右前
    sim.setObjectOrientation(leftMotor, ontology, angle)
    sim.setObjectOrientation(rightMotor, ontology, angle)
    # 輸入一個變數改變前輪方向

def controlAngle(z, direction):
    if direction == 'forward':
        if keyboard.is_pressed('a'):
            setAngle(-z)
        elif keyboard.is_pressed('d'):
            setAngle(z)
        else:
            setAngle(0)
    elif direction == 'backward':
        if keyboard.is_pressed('a'):
            setAngle(z)
        elif keyboard.is_pressed('d'):
            setAngle(-z)
        else:
            setAngle(0)

def turnover():
    floor = sim.getObject('/Floor')
    player1 = sim.getObject(player)
    a = sim.getObjectOrientation(player1, floor)
    b = sim.getObjectPosition(player1, floor)
    a[0] = 0
    a[1] = 0
    b[2] = 0.3
    sim.setObjectPosition(player1, floor, b)
    sim.setObjectOrientation(player1, floor, a)

def playerControl(x, z):
    if keyboard.is_pressed('w'):
        if keyboard.is_pressed('a'):
            setVelocity(-x/2, -x, -x/2, -x)  # 減少左轉時的速度
        elif keyboard.is_pressed('d'):
            setVelocity(-x, -x/2, -x, -x/2)  # 減少右轉時的速度
        else:
            setVelocity(-x, -x, -x, -x)  # 調整前進方向
        controlAngle(z, 'forward')
    elif keyboard.is_pressed('s'):
        if keyboard.is_pressed('d'):
            setVelocity(x/2, x, x/2, x)  # 減少左轉時的速度
        elif keyboard.is_pressed('a'):
            setVelocity(x, x/2, x, x/2)  # 減少右轉時的速度
        else:
            setVelocity(x, x, x, x)  # 調整後退方向
        controlAngle(z, 'backward')
    elif keyboard.is_pressed('d'):
        setVelocity(-x/2, x/2, -x/2, x/2)  # 減少左轉時的速度
    elif keyboard.is_pressed('a'):
        setVelocity(x/2, -x/2, x/2, -x/2)  # 減少右轉時的速度
    elif keyboard.is_pressed('space'):
        turnover()
    elif keyboard.is_pressed('q'):
        # 停止模擬
        sim.stopSimulation()
    else:
        setVelocity(0, 0, 0, 0)
        setAngle(0)

while True:
    if keyboard.is_pressed('shift'):
        playerControl(v + 4, z - 20)
    else:
        playerControl(v, z)