#GENERATE INPUT 
#Generate random timestamp within a certain range 
#Generate random direction in degrees 
#Choose random small_vehicle or large_vehicle 
#Choose random vehicle count 
import random
#1586633114988,small_vehicle,1.0,318.0
vehicle_types = ['small_vehicle','large_vehicle']
text_file = open("chunk50.txt", "w")

for i in range(1000):
  direction = random.randint(0, 360)
  timestamp = random.randint(1564643005310, 1586728880860)
  vehicle_count = random.randint(0, 10)
  vehicle_type = random.choice(vehicle_types)
  text_file.write("%s,%s,%d,%s\n" % (str(timestamp), vehicle_type, vehicle_count, str(direction) ) )

text_file.close()
print("done")