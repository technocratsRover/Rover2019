host = ""
port = 1605
from socket import *
import serial
ser = serial.Serial('/dev/ttyACM0',9600)
s = socket(AF_INET, SOCK_STREAM)
s.bind((host, port))
print("Server has started..")
s.listen(1)
q, addr = s.accept()
print("Client connected")
data = ""
print("Recieving Data")
while (data != "exit"):
    data = q.recv(1024)
    data = data.strip().decode('ascii')
    ser.write(bytes(data,'UTF-8'))
#    print(data)
ser.close()
s.close()
