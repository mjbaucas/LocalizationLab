# Import libraries
from __future__ import division 
import os
import re
import subprocess
from matplotlib import pyplot as pl

# Define coordinates and measurements
x_max = 4.27 # Change this based on actual length of space in x-axis created by anchors
y_max = 3.35 # Change this based on actual length of space in y-axis created by anchors 
nodes = [0, 0, x_max, 0, 0, y_max, x_max, y_max]

# Function for obtaining RSS values of anchors
def findRSSI():
    # Read RSSI values and format to string
    result = subprocess.check_output("sudo iwlist wlan0 scan | grep -E \"SSID|level\"", shell=True).decode('utf-8')
    result_string = re.split("\s|\n|=|_|:", result)
    result_string = list(filter(None, result_string))
    
    # Assign anchor RSSI values to list
    values = [0,0,0,0]
    i = 0 
    for i in range(len(result_string)):
        if result_string[i] == "\"Anchor":  
            if result_string[i+1] == "1\"":
                values[0] = int(result_string[i-3])
            if result_string[i+1] == "2\"":
                values[1] = int(result_string[i-3])
            if result_string[i+1] == "3\"":
                values[2] = int(result_string[i-3])
            if result_string[i+1] == "4\"":
                values[3] = int(result_string[i-3])
                
    # print(values) # Debug: Check values obtained
    return values

# Calculatin function for the pathloss distance based on the rssi input
def pathloss(rssi):
    C = -50.0 # Approximately the expected RSSI value at 1 metre
    n = 2.0   # Pathloss exponent (free space = 2)
    
    distance = 10.0**((rssi - C) / (-10.0 * n)) # Distance formula given RSSI
    # print(distance) # Debug: Check distance calculated
    return distance

# Trilateration function for the localization of the point of interest
def trilateration(d1, d2, d3, p, q, r):
    x = (d1**2 - d2**2 + p**2) / (2.0 * p)                          # Calculate x coordinate 
    y = ((d1**2 - d3**2 + q**2 + r**2) / (2.0 * r)) - ((q / r) * x) # calculate y coordinate 
    
    reciever = [x,y]
    return reciever
    
# Obtain RSSI and corresponding distances
values = findRSSI()  
d1 = pathloss(values[0]) 
d2 = pathloss(values[1]) 
d3 = pathloss(values[2]) 

# Establishing known points on coordinate plane assuming anchors are exactly on the established axes
p = x_max # Known distance between anchor in the x axis and origin
q = 0      # This is zero because anchors are assumed to be exactly on the axes 
r = y_max # Known distance between nachor in the y axis and origin 

# Obtain point of interest using trilateration
reciever = trilateration(d1, d2, d3, p, q, r)
print(reciever) # Debug: Check reciever coordinate

# Plot anchors and reciever on the coordinate plane
pl.plot(nodes[0], nodes[1], 'bs')       # Anchor 1
pl.plot(nodes[2], nodes[3], 'rs')       # Anchor 2 
pl.plot(nodes[4], nodes[5], 'gs')       # Anchor 3
pl.plot(nodes[6], nodes[7], 'ys')       # Anchor 4
pl.plot(reciever[0], reciever[1], 'k^') # Reciever 

pl.xlabel('X')
pl.ylabel('Y')
pl.legend(('Anchor 1', 'Anchor 2', 'Anchor 3', 'Anchor 4', 'Reciever'))
pl.grid()
pl.show()
pl.savefig("lab3.png")