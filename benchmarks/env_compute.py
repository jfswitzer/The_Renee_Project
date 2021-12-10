import socketio
import time
import os
import sys
import json
from zipfile import ZipFile
contents = [{'filename': 'main/', 'bytes': ''}, {'filename': 'main/main.sh', 'bytes': 'python3 main.py\n'}, {'filename': 'main/main.py', 'bytes': "def fibonacci(n):\n    if n < 1:\n        print('err')\n        return -1\n    if n==1 or n==2:\n        return 1\n    return fibonacci(n-1)+fibonacci(n-2)\nprint(fibonacci(30))\n"}] 
#spoof of fib contents
def process_zip_task(contents):
    owd = os.getcwd()
    zipObj = ZipFile('temp.zip', 'w')
    for obj in contents:
        fn = obj['filename']
        byts = obj['bytes']
        zipObj.writestr(fn,byts)
    zipObj.extractall(path='temp')
    os.system('rm temp.zip')    
    os.chdir(owd+'/temp/main')
    os.system('mkdir output_tmp')
    os.system('chmod u+x main.sh')
    os.system('./main.sh > ../../output')
    os.system('echo $? > ../../status')
    os.system(f'mv output_tmp {owd}') #hmm what happens if no output folder, need to zip
    os.chdir(owd)
    os.system('rm -rf temp')
start = time.time()
process_zip_task(contents)
end = time.time()
print(end-start)
