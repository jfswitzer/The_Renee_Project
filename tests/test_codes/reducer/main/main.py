#!/usr/bin/env python3
  
import sys
from collections import defaultdict
import sys
word_count = defaultdict(int)
for i in range(50):
  filename="chunksout/chunk"+str(i)+".txt"
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

