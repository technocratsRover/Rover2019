import serial
import time
class RoverGps():
	def __init__(self):
		self.ser = serial.Serial()
		self.ser.baudrate = 9600
		self.ser.port = "/dev/serial0"
		self.ser.timeout=10
		self.i = 0
	def getGpsData(self):
		while 1:
			try:
				self.ser.close()
				self.ser.open()
				self.ser.flush()
				self.i = self.ser.readline()
#				print(str(str(self.i).split(',')[0])[2:])
				if str(self.i).split(',')[0][2:]=='$GPGGA':
					print (str(self.i).split(',')[2], str(self.i).split(',')[4])
					return [float(str(self.i).split(',')[2])/100, float(str(self.i).split(',')[4])/100]
                                #print i.split(',')[4]
#                               break
#                       print i
#                       ser.close()
			except KeyboardInterrupt as e:
				print("kkkk")
#                       print(e)
				self.ser.close()
				break
			except Exception as e:
				print("Waiting")
#				print(e)
				self.ser.close()
				continue
			self.ser.close()

a = RoverGps()
print(a.getGpsData())
