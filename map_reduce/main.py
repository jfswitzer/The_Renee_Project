import sys
from lib import *

if len(sys.argv)<2:
    print("Please specify map or all")
    quit()
chunks = {}
for i in range(1,50):
    chunks[f"c{i}"]=f"chunk{i}.txt"
mr = MapReduce("streetlight_mapper.py","reducer_example.py",2,chunks,100)
mr.run(sys.argv[1])
