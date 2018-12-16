import gps
import serial
import threading

#! =============================
#! Dont touch the file behnchod
#! =============================
class RoverGps():
  def __init__(self):
    # self.devicePath = device
    #! Uncomment when running with gps module
    self.connectGPS()
    self.lat=None
    self.lon=None
    self.threadStart()
    self.error=False
    # #! debug only
    # self.x=80
    # self.y=20
    # self.count=0
    # #! debug end
  
  def threadGpsValues(self):
    while True:
      report=self.session.next()
      # print(report)
      if hasattr(report, 'lon'):
        self.lon=round(float(report['lon'])*1000000)/1000000
      if hasattr(report, 'lat'):
        self.lat=round(float(report['lat'])*1000000)/1000000


  def threadStart(self):
    self.gpsThread = threading.Thread(target=self.threadGpsValues)
    self.gpsThread.start()
      
  def connectGPS(self):
    try:
      # GPS Socket
      self.session = gps.gps("localhost", "2947")
      self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    except OSError as e:
      self.error=True
    except Exception as e:
      raise e
  
  def getGpsData(self):
    # print(self.lat,self.lon)
    # Degub Only
    # self.count+=1
    # if self.count==100:
    #   self.count=0
    #   self.x+=1
    #   self.y+=1
    # return [self.x, self.y]
    # Debug end
    # print(self.session)
    # print(self.session.next())
    if self.error:
      return "Error: GPS disconnected!"
    else:
      return [self.lat, self.lon]
    
