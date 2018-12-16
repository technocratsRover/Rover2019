host = "192.168.43.94"
port = 1605
from socket import *
import serial
print("Initializing connection...")
s = socket(AF_INET, SOCK_STREAM)
s.connect((host, port))
print("Connected with server!")
arduinoData = serial.Serial("com11",9600)
data = ""
while (data != "exit"):
    if (arduinoData.inWaiting() > 0):
        data = arduinoData.readline()
        s.send(data)
arduinoData.close()
s.close()