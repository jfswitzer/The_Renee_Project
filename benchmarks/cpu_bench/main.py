import sys
import time
import logging
from threading import Thread
logging.basicConfig(filename="cpu_log.csv",format='%(levelname)s,%(message)s', level=logging.DEBUG)

def fibonacci(n):
    if n < 1:
        print('err')
        return -1
    if n==1 or n==2:
        return 1
    return fibonacci(n-1)+fibonacci(n-2)
def test(i):
    for _ in range(int(sys.argv[2])):
        st = time.time()
        fibonacci(30)
        e = time.time()
        diff = e-st
        logging.info(str(diff)+','+str(i))
        

for i in range(int(sys.argv[1])):
    thread = Thread(target = test, args = (i,))
    thread.run()
