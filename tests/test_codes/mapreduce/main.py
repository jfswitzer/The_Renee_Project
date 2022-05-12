#!/usr/bin/env python3  
  
import sys
import string

import csv
import time
  
from collections import defaultdict


for i in range(50):
  filename="chunks/chunk"+str(i)+".txt"
  text_file = open(filename, "r+")
  Lines = text_file.readlines()
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
    filename = "chunk" + str(i) + "c.txt"
    f = open(filename, "a")
    f.write("%s\t%s\t%d\t%s\n"%(datetime, vehicle_type, int(float(vehicle_count)), direction))
    f.close()


word_count = defaultdict(int)
for i in range(50):
    filename="chunk"+str(i)+"c.txt"
    text_file = open(filename, "r+")
    Lines = text_file.readlines()
    for line in Lines:
        #print(line)
        line = line.strip()
        words = line.split()
    # print("words")
        if len(words) < 4:
            continue
    # print(words)
        date = words[0]
        hour =  words[1]
        vehicle_type = words[2]
        count = words[3]
        count = int(count)
        word_count[date+" "+hour] += count
    for date, count in word_count.items():
        filename="chunkreduce.txt"
        text_file = open(filename, "a")
        text_file.write('%s\t%s'% (date, count))
        text_file.close()
        #print('%s\t%s' % (date, count))

