#luma.oled provides a Python3 interface to OLED matrix displays
#with SSD1322 controllers to connect with Raspberry Pi 
#https://luma-oled.readthedocs.io/en/latest/intro.html

#use 'luma-env' virtual environment
#run the following the terminal to run script via terminal:
#source /home/elrhmo/luma-env/bin/activate && python3 /home/elrhmo/bus_departure_board/textdisplay.py

#note, script runs automatically when your Raspberry Pi boots up, using the rc.local file
#run sudo nano /etc/rc.local in the terminal to edit it

from luma.core.render import canvas
from luma.core.interface.serial import spi
from luma.core import cmdline
from luma.oled.device import ssd1322

from datetime import datetime
import requests
from time import sleep


serial = spi(device=0, port=0) 
device = ssd1322(serial)


while True:
    #getting the current time
    time = str(datetime.now().strftime("%H:%M"))
    #time_sec_1 = str(datetime.now().strftime("%H:%M:%S"))

    #get bus departure data from get_data module
    try:
        from get_data import get_bus_data
        departure_list = get_bus_data()
        # Ensure departure_list always has 3 elements with 4 sub-elements each
        while len(departure_list) < 3:
            departure_list.append([''] * 4)  # Append empty sub-lists if necessary
            # If there are fewer than 4 elements in any sub-list, extend it with empty strings
            for sublist in departure_list:
                while len(sublist) < 4:
                    sublist.append('')
    except Exception as e:
        print("An error occurred:", str(e))
        print("Waiting for 1 minute before rerunning...")
        with canvas(device) as draw:
            draw.multiline_text((0, 0),"An error occurred:", fill="white")
            draw.multiline_text((0, 15),str(e), fill="white")
            draw.multiline_text((0, 45),"Waiting for 1 minute before getting data from TfL", fill="white")            
        time.sleep(60)  # Wait for 1 minute before rerunning 

    

    with canvas(device) as draw:
        #draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.multiline_text((0, 0),departure_list[0][0], fill="white")   
        draw.multiline_text((10, 0),departure_list[0][1], fill="white") 
        draw.multiline_text((40, 0),departure_list[0][2], fill="white")
        draw.multiline_text((220, 0),departure_list[0][3], fill="white")
        draw.multiline_text((0, 15),departure_list[1][0], fill="white")
        draw.multiline_text((10, 15),departure_list[1][1], fill="white")
        draw.multiline_text((40, 15),departure_list[1][2], fill="white")
        draw.multiline_text((220, 15),departure_list[1][3], fill="white")
        draw.multiline_text((0, 30),departure_list[2][0], fill="white")
        draw.multiline_text((10, 30),departure_list[2][1], fill="white")
        draw.multiline_text((40, 30),departure_list[2][2], fill="white")
        draw.multiline_text((220,30),departure_list[2][3], fill="white")
        draw.multiline_text((125, 50), time, fill="white",  align="center")

                
        #testing the the time it takes to run the while llop
        #time_sec_2 = str(datetime.now().strftime("%H:%M:%S"))
        #print(f"Time 1: {time_sec_1}")
        #print(f"Time 2: {time_sec_2}")
        
        #print(departure_list)
        
        #reruns code within the while loop every 5 seconds
        sleep(5)
