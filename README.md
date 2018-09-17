# IRC CHALLENGE 2019  
### CSE GROUP

The CSE Group of VIT CHENNAI MARKS ROVER will handle the following modules : 
* Streaming of Visual Feed
* Object Detection 
* GPS
* Web Interface

#### STREAMING OF VISUAL FEED  

There will be three cameras that will be used to record live video footage from the rover. These cameras will be the ARMCAM, the FRONTCAM and the REARCAM. The FRONTCAM and the REARCAM will be connected to a single Raspberry Pi and the ARMCAM will be handled only by a single pi. 

The Raspberry Pi with the two cameras contains a shell script **double_stream** that runs when the Pi boots and activates the two cameras for video streaming. The script contains the command to start motion and execute a python script. The motion command activates the usb-camera and the pyhton script activates the Pi Camera.  
The configuration in the file _motion.conf_ are set according to the required output and the capibilities of the usb-camera. This feed is shown at the port number 8081.  
The pyhton script _rpi_camera_surveillance_system_ streams the video feed from the Pi Camera to the port number 8000.  

The HTML page _frame divide testing_ uses frame to divide the page into three parts for the feed. In each frame another HTML page is embedded which contains the feed of that particular camera. 

#### OBJECT DETECTION


#### WEB INTERFACE
