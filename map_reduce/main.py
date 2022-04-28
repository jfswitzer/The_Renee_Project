from lib import *

mr = MapReduce("mapper_example.py","reducer_example.py",2,{"c1":"chunk1.txt","c2":"chunk2.txt"},100,"local.json")
mr.run()
