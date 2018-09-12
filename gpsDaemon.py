import select
import sys
from time import sleep
import socket
import math
import os
import argparse

err = ''
isAuto=False
parser = argparse.ArgumentParser(description='Connect to server')
# parser.add_argument('hostname', type=str)
parser.add_argument('port', type=int)

args = parser.parse_args()

# HOST = args.hostname
PORT = args.port
BUFFER = 1024

daemon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
daemon.bind(('', PORT))

# FORMAT 	for input data
# INIT 		for initial location
# ADD 		to append location
# CURRENT 	to get current location
# EXIT 		to close the program
location = []
logs=[]
currentLocation=None
nextLocation=None

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])^2+(p1[1]-p2[1])^2)

print("Daemon Started! Waiting for service.. ", PORT)

daemon.listen(1)
daemon, address = daemon.accept()
print('Service connected!')


while True:
    sleep(0.1)
    os.system('clear')
    readable, _, _ = select.select([sys.stdin, daemon], [], [], 0)
    for service in readable:
        if service is daemon:
            # Parse the input
            try:
                data = daemon.recv(BUFFER)
                data = data.decode('ascii').rstrip().split(' ')
            except UnicodeDecodeError:
                pass
        elif service is sys.stdin:
            data = sys.stdin.readline().rstrip().split(' ')
        else:
            pass
        operation = data[0]
        if operation in ['INIT', 'ADD', 'CURRENT']:
            if len(data) >= 3:
                values = [float(x) for x in data[1:]]
            else:
                data = 'ERR'
                err = 'Size of argument mismatch!'

        if operation=='INIT':
            location.clear()
            location.append([values[0], values[1]])
            currentLocation=[values[0], values[1]]
        elif operation=='ADD' and len(location)>0 and data[1] not in location:
            location.append([values[0], values[1]])
            if not nextLocation:
                nextLocation=[values[0], values[1]]
        elif operation=='CURRENT':
            currentLocation=[values[0], values[1]]
            if nextLocation and abs(currentLocation[0] - nextLocation[0])<2 and abs(currentLocation[1] - nextLocation[1])<2 and len(location)>2:
                try:
                    nextLocation = location[location.index(nextLocation)+1]
                except IndexError:
                    print("FINISHED!")
                    daemon.close()
                    sys.exit()
                print("New: ", nextLocation)
        elif operation=='LOG':
            logs.append(currentLocation)
        elif operation=='CLEAR':
            location.clear()
            location.append(currentLocation)
            nextLocation=[]
        elif operation=='REMOVE':
            del location[int(data[1])]
        else:
            err = 'Unknown command!' + str(data)


    print("Error: ", err)
    print("\nDetails...")
    print("Locations:", len(location))
    for i in location:
        print(i, end=', ')
    print("\nLOG:", end='')
    for i in logs:
        print(i, end=', ')
    print("\nCurrent:", currentLocation)
    print("Next:", nextLocation)
    sys.stdout.write('Command: ')
    # sys.stdout.write(sys.stdin.readline())
    sys.stdout.flush()
        

