from tkinter import *
import select
import sys
from time import sleep
import socket
import math
import os
import argparse
import threading

# ================
# Global Variables
# ================
BUFFER = 1024
location=[]
log=[]
queue=[]
client_list=[]

# =============
# System Parser
# =============
parser = argparse.ArgumentParser(description='Connect to server')
parser.add_argument('port', type=int)
args = parser.parse_args()

# HOST = args.hostname
PORT = args.port
BUFFER = 1024

# ========================
# Start the Station Server
# ========================
daemon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
daemon.bind(('', PORT))
client_list.append(daemon)

# Function for threading
def recieve():
  data=''
  t = threading.currentThread()
  
  while client_list:
    readable, _, _ = select.select(client_list, [], [], 0)
    for socket in readable:
      if socket is daemon:
        # New connection is requested!
        connection, addr = daemon.accept()
        client_list.append(connection)
      else:
        try:
          data = socket.recv(BUFFER).decode('ascii').rstrip().split()
        except Exception as e:
          print(e)
        
        if not data:
          # Clinet has closed the connection
          print("Client: ", socket.getpeername(), " Disconnected!")
          socket.close()
          client_list.remove(socket)
        else:
          app.updateData(data)

# =====================
# GUI Application Class
# =====================
class Application(Frame):
  # Contructor
  def __init__(self, master=None):
    Frame.__init__(self, master)
    # Variables
    self.location=[]
    self.log=[]
    self.master=master
    self.currentLocation = None
    self.nextLocation = None
    self.textLocationValue=[]
    self.pastExecutedCommand = 'None'
    self.auto=False
    self.autoState='normal'
    self.data='None'
    
    master.geometry('600x400')
    self.initMenu()
    self.infoWidget()
    self.master.protocol('WM_DELETE_WINDOW', self.clientExit)

  # Menu
  def initMenu(self):
    menu = Menu(self.master)
    self.master.config(menu=menu)

    file = Menu(menu)
    file.add_command(label="Exit", command=self.clientExit)
    menu.add_cascade(label="File", menu=file)

    edit=Menu(menu)
    edit.add_command(label="Undo")
    menu.add_cascade(label="Edit", menu=edit)

  # The main information widget
  def infoWidget(self):
    self.master.title("GUI")                                        # changing the title of our master widget      
    self.pack(fill=BOTH, expand=1)                                  # allowing the widget to take the full space of the root window
    # Auto button
    self.autoButton = Button(self, text='Auto', command=self.toggleAuto)
    self.autoButton.place(x=420, y=20)
    self.textAuto = Label(self, text=self.autoState)
    self.textAuto.place(x=500, y=20)

    # Current Location
    self.textCurrLab = Label(self, text='Current Location: ')
    self.textCurrLab.place(x=30, y=20)

    self.textCurrVal = Label(self, text=self.currentLocation)
    self.textCurrVal.place(x=150, y=20)

    # Next Location
    self.textNextLab = Label(self, text='Next Location: ')
    self.textNextLab.place(x=30, y=50)

    self.textNextVal = Label(self, text=self.nextLocation)
    self.textNextVal.place(x=150, y=50)

    # Location
    self.LocationList()

    # Command Input
    self.textCommandLab = Label(self, text="Command: ")
    self.textCommandLab.place(x=30, y=100)
    self.inputCommand = Entry(self, width=50, state=self.autoState)
    self.inputCommand.place(x=100, y=100)

    self.inputButton = Button(self, text='Execute', command=self.parseCommand)
    self.inputButton.place(x=420, y=100)

    # Past executed
    self.textPastExeutedLabel = Label(self, text='Previous Command: ')
    self.textPastExeutedLabel.place(x=30, y=150)
    self.textPastExeutedVal = Label(self, text=self.pastExecutedCommand)
    self.textPastExeutedVal.place(x=170, y=150)

    # Data
    self.textData = Label(self, text=self.data)
    self.textData.place(x=400, y=300)

    # Location
    self.textLocationLabel = Label(self, text="Location: ")
    self.textLocationLabel.place(x=30, y=200)

  # Labels for list of locations
  def LocationList(self):
    # Prints the location list
    print(len(self.location))
    while len(self.textLocationValue)> 0:
      self.textLocationValue[-1].destroy()
      self.textLocationValue.pop()
    self.textLocationValue=[]
    for i in range(len(self.location)):
      tempLabel = Label(self, text=str(str(self.location[i][0]) + " "+ str(self.location[i][1])))
      self.textLocationValue.append(tempLabel)
      self.textLocationValue[-1].place(x=30, y=220+(i+1)*20)

  # Parse the instructions
  def parseCommand(self):
    print(self.inputCommand.get())
    self.pastExecutedCommand = self.inputCommand.get()
    self.textPastExeutedVal.config(text=self.pastExecutedCommand)
    daemon.send(self.pastExecutedCommand.encode('ascii'))
    self.updateData(self.pastExecutedCommand.split(' '))

  # Toggle auto or normal mode
  def toggleAuto(self):
    self.auto=not self.auto
    if self.auto:
      self.autoState='disabled'
    else:
      self.autoState='normal'
    self.inputCommand['state']=self.autoState
    self.textAuto.config(text=self.autoState)

  # Update the GUI witht the provided data

  def updateDataGPS(self, data):
    operation = data[0]

    if operation in ['INIT', 'ADD', 'CURRENT']:
      if len(data) >= 3:
        values = [float(x) for x in data[1:]]
      else:
        operation = 'ERR'
        err = 'Size of argument mismatch!'

    self.data = data
    self.textData.config(text="Recieved: "+str(self.data))

    if operation=='INIT':
      self.location.clear()
      self.location.append([values[0], values[1]])
      self.LocationList()

      self.currentLocation=[values[0], values[1]]
      self.textCurrVal.config(text=str(values[0])+" N, "+str(values[1]))

      self.nextLocation=None
      self.textNextVal.config(text='')
    elif operation=='ADD' and len(self.location)>0 and data[1] not in self.location:
      self.location.append([values[0], values[1]])

      self.LocationList()

      if not self.nextLocation:
        self.nextLocation=[values[0], values[1]]

        self.textNextVal.config(text=str(self.nextLocation[0])+" N, "+str(self.nextLocation[1]))

    elif operation=='CURRENT':
      self.currentLocation=[values[0], values[1]]
      self.textCurrVal.config(text=str(values[0])+" N, "+str(values[1]))
      if self.nextLocation and abs(self.currentLocation[0] - self.nextLocation[0])<2 and abs(self.currentLocation[1] - self.nextLocation[1])<2 and len(self.location)>2:
        try:
          self.nextLocation = self.location[self.location.index(self.nextLocation)+1]
          self.textNextVal.config(text=str(self.nextLocation[0])+" N, "+str(self.nextLocation[1]))
        except IndexError:
          print("FINISHED!")
          daemon.close()
          sys.exit()
        print("New: ", self.nextLocation)
      
    elif operation=='LOG':
      self.logs.append(self.currentLocation)
    elif operation=='CLEAR':
      self.location=[]
      self.location.append(self.currentLocation)

      self.nextLocation=None
      self.textNextVal.config(text='')

      self.LocationList()
    # !Code is incomplete
    elif operation=='REMOVE':
      del self.location[int(data[1])]
    else:
      err = 'Unknown command!' + str(data)

  def updateDataSensor(self, data):
    pass
  def updateData(self, data):
    typeOfData=data[0]
    if typeOfData=='$GPS':
      self.updateDataGPS(data[1:])
    elif typeOfData=='$SENSOR':
      self.updateDataSensor(data[1:])
    else:
      print('Unknown Type: ', typeOfData. " recieved!")
      
    

  # Function to handle exit
  def clientExit(self):
    # daemon.close()
    print("Exiting...")
    self.master.destroy()
    recieveThread.run=False
    recieveThread.join()
    print("Thread: ", recieveThread.isAlive())
    sys.exit()


print("Daemon Started! Waiting for service.. ", 47776)
daemon.listen(1)
daemon, address = daemon.accept()
print("Connection Accepted!")
recieveThread = threading.Thread(target=recieve)
recieveThread.start()

root = Tk()
app = Application(master=root)

root.mainloop()
