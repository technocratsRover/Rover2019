from nanpy import ArduinoApi, SerialManager
from time import sleep
import threading


# FRONT BACK RIGHT LEFT
motorState = [False, False, False, False]

def resetAllMotors():
  for i in range(len(motorState)):
    motorState[i]=False

# The motors pins are pinOffset + 0, pinOffset + 1, pinOffset + 2, pinOffset + 3
pinOffset = 7

# Connect to arduino
try:
  connection = SerialManager("/dev/ttyUSB0")
  a = ArduinoApi(connection=connection)
except:
  print("Failed to connect to arduino!")

def motor():
  print("Motor thread Started!")
  while True:
    for i in range(len(motorState)):
      if motorState[i]:
        a.digitalWrite(pinOffset+i, a.HIGH)
      else:
        a.digitalWrite(pinOffset+i, a.LOW)

# def input():
#   while True:
#     print("Enter command: ", end='')
#     motorNum = int(input().rstrip)
#     try:
#       motorState[motorNum]=True
#     except IndexError:
#       if motorNum ==  4:
#         resetAllMotors()
#       else:
#         print("Invalid motor Number, Valid options: [0, 1, 2, 3, 4]")

motorThread = threading.Thread(target=motor)
# inputThread = threading.Thread(target=input)
motorThread.start()
# inputThread.start()
while True:
  print("Enter command: ", end='')
  try:
    motorNum = int(input())
  except ValueError:
    print("Enter an integer!, Valid options: [0, 1, 2, 3, 4]")
    continue
  try:
    resetAllMotors()
    motorState[motorNum]=True
  except IndexError:
    if motorNum ==  4:
      resetAllMotors()
    else:
      print("Invalid motor Number, Valid options: [0, 1, 2, 3, 4]")
