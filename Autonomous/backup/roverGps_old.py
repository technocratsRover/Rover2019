#import gps
import serial
import threading

# ! =====================================
# ! DO NOT CHANGE, FIX OTHER THINGS FIRST
# ! =====================================

class RoverGps():
  def __init__(self, device):
    self.ser = serial.Serial()
    self.ser.baudrate = 9600
    self.ser.port = device

    self.i = 0            # ! Define i
#    self.connectGPS()
    self.lat=0
    self.lon=0
    self.threadStart()


    # ! debug only
    # self.x=80
    # self.y=20
    # self.count=0
    # ! debug end
  
  # ? If possible remove the opening and closing to another function
  def threadGpsValues(self):
    while True:
      try:  
        self.ser.close()
        self.ser.open()
        try:
          self.ser.flush()
        except:
          self.ser.close()
          self.ser.open()
        self.i = self.ser.readline()

        if str(self.i).split(',')[0][2:]=='$GPGGA':
          # print ("Updated:", str(self.i).split(',')[2], str(self.i).split(',')[4])
          self.lat = float(str(self.i).split(',')[2])/100
          self.lon = float(str(self.i).split(',')[4])/100
      except serial.serialutil.SerialException:
        self.ser.close()



  def threadStart(self):
    self.gpsThread = threading.Thread(target=self.threadGpsValues)
    self.gpsThread.start()
      
  def getGpsData(self):
    return [self.lat, self.lon]

    #def connectGPS(self):
    #  try:
    #    # GPS Socket
    #    self.session = gps.gps("localhost", "2947")
    #    self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    #  except Exception as e:
    #    raise e
    
# ! =====================================
# ! DO NOT CHANGE, FIX OTHER THINGS FIRST
# ! =====================================