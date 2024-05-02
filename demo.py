# Import libraries
import os
import re
import subprocess

# Function for obtaining RSS values of anchors
def findRSSI():
    # Read RSSI values and format to string
    result = subprocess.check_output("sudo iwlist wlan0 scan | grep -E \"SSID|level\"", shell=True).decode('utf-8')
    result_string = re.split("\s|\n|=|_|:", result)
    result_string = list(filter(None, result_string))
    
    # Assign anchor RSSI values to list
    value = 0
    i = 0 
    for i in range(len(result_string)):
        if result_string[i] == "\"Anchor":  
            if result_string[i+1] == "1\"":
                values = int(result_string[i-3])
                
    # print(value) # Debug: Check value obtained
    return value

# Calculation function for the pathloss distance based on the rssi input
def pathloss(rssi):
    C = -50.0 # Approximately the expected RSSI value at 1 metre
    n = 2.0   # Pathloss exponent (free space = 2)
    
    distance = 10.0**((rssi - C) / (-10.0 * n)) # Distance formula given RSSI
    # print(distance) # Debug: Check distance calculated
    return distance
    
# Obtain RSSI and corresponding distances
value = findRSSI()  
distance = pathloss(value) 
print("RSSI: " + value + " dBm")
print("Distance: " + distance + " metres")