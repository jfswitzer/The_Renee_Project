#!/usr/bin/env python3  
  
import sys
import string

import csv
import time

def mapper(filename):
  text_file = open(filename, "r+")
  Lines = text_file.readlines()[1:] #skip the 1st line
  for line in Lines:
    line = line.strip()
    words = line.split(",")
    if(len(words) < 4):
      continue
    vehicle_type = words[1]
    vehicle_count = words[2]
    degrees = words[3]

    #convert degrees to word
    degrees_int = (int)((float)(degrees))
    if degrees_int <= 315 and degrees_int >= 225:
      direction = "West"
    elif degrees_int > 315 or degrees_int <= 45:
      direction = "North"
    elif degrees_int > 45 and degrees_int <= 135:
      direction = "East"
    else:
      direction = "South"


      #timestamp
      timestamp = int(words[0])/1000

      datetime = time.strftime('%Y-%m-%d %H:00', time.localtime(timestamp))
      print("%s\t%s\t%d\t%s"%(datetime, vehicle_type, int(float(vehicle_count)), direction))
      #n = text_file.write("%s\t%s\t%d\n"%(datetime, vehicle_type, int(float(vehicle_count))))
      # n = text_file.write("%s\t%s\t%d\t%s\n"%(datetime, vehicle_type, int(float(vehicle_count)), direction))


