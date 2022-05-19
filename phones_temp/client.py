import socketio
import time
import requests
import os
import sys
import json
import threading
from zipfile import ZipFile

ENDPOINT = 'localhost'
with open("../config.json") as f:
    ENDPOINT = json.load(f)["conductor_IP"]
SERVER_ENDPOINT = f"http://{ENDPOINT}:5000"
STATUS_FAILED = 2
STATUS_SUCCEDED = 3

# get the device id
# Note: device id 0 is registered for testing, real devices should use ids >= 1
with open("./id.txt", "r") as f:
    device_id = int(f.readline())

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def disconnect():
    print('disconnected from server')

@sio.on("task_submission")
def task_submission(data):
    # Check if this is for this deviceid
    if device_id != data['device_id']:
        return

    job_id = data['job']['id']
    sio.emit('task_acknowledgement', {'device_id': device_id, 'job_id' : job_id})

    th = threading.Thread(target=handle_received_task,args=(data,job_id))
    th.start()
    
def handle_received_task(data,job_id):
    print('Working on job id={}: '.format(job_id))
    idstr = process_zip_task(data['job']['code_bytes'],job_id)
    result = ""
    status = 0
    if idstr!='':
        with open(f"./output{idstr}", "r") as f:
            result += f.read()
        with open(f"./status{idstr}", "r") as f:
            status = int(f.readline())
        print(f'removing output and status for {idstr}')
        os.system(f'rm ./output{idstr}')
        os.system(f'rm ./status{idstr}')                
    else:
        status = -1
    # Once the job succeeds/fails, notify the server
    status = STATUS_SUCCEDED if status == 0 else STATUS_FAILED
    resp = requests.post(f"{SERVER_ENDPOINT}/jobs/{job_id}/update_status/", json={"device_id" : device_id, "status" : status, "result" : result}).json()

    print("Response from notifying server of job status: {}".format(status))
    print(resp)

def process_git_task(url): #not really in use anymore
    # clone the git repo
    os.system('git clone {}'.format(url))
    # get the directory
    directory = url.split('/')[-1].replace('.git', '')
    # run the file and store in a file
    os.system('cp cli.py ./{}/'.format(directory))    
    os.system('./{}/main.sh > ./output'.format(directory))
    # check the exit code and store in a file
    os.system('echo $? > ./status')
    # remove the git repo
    os.system('rm -rf {}'.format(directory))
    return True

def process_zip_task(contents,job_id,persist=''):
    timestamp = str(time.time())
    idstr = f'{timestamp}{job_id}'
    owd = os.getcwd()
    print(f'Creating a temp for {idstr}')
    zipObj = ZipFile(f'temp{idstr}.zip', 'w')
    for obj in contents:
        try:
            fn = obj['filename']
            byts = obj['bytes']
            zipObj.writestr(fn,byts)
        except TypeError:
            return '' #empty job
    try:
        zipObj.extractall(path=f'temp{idstr}')
    except EOFError:
        return ''

    os.system(f'cp cli.py temp{idstr}/main/')
    os.system(f'rm temp{idstr}.zip')    
    os.system(f'chmod u+x {owd}/temp{idstr}/main/main.sh')
    os.system(f'{owd}/temp{idstr}/main/main.sh {owd}/temp{idstr}/main/ > {owd}/temp{idstr}/main/output{idstr}')
    os.system(f'echo $? > {owd}/temp{idstr}/main/status{idstr}')
    os.system(f'mv {owd}/temp{idstr}/main/output{idstr} .')
    os.system(f'mv {owd}/temp{idstr}/main/status{idstr} .')    
    os.system(f'rm -rf temp{idstr}')
    return idstr


sio.connect(f"{SERVER_ENDPOINT}/?device_id={device_id}")
sio.wait()
