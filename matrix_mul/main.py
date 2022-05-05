import sys
import random
N = int(sys.argv[1])
X = [[0]*N]*N
Y = [[0]*N]*N
result = [[0]*N]*N
for i in range(N):
   for j in range(N):
      X[i][j] = random.randint(1,N)
      Y[i][j] = random.randint(1,N)      
# iterate through rows of X
for i in range(len(X)):
   # iterate through columns of Y
   for j in range(len(Y[0])):
       # iterate through rows of Y
       for k in range(len(Y)):
           result[i][j] += X[i][k] * Y[k][j]

for r in result:
   print(r)
