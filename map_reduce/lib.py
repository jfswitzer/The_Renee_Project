import zipfile
import os
import shutil
import threading
import requests
import sys
import time
from halo import Halo
import mr_db
import json
JOB_STATUS_POLL_INTERVAL_SECS = 0.2
ENDPOINT = 'localhost'
with open("../config.json") as f:
    ENDPOINT = json.load(f)["conductor_IP"]
SERVER_ENDPOINT = f"http://{ENDPOINT}:5000"
#SERVER_ENDPOINT = "http://192.168.1.65:5000" #generalize
submit_job_url = f"{SERVER_ENDPOINT}/jobs/submit/"
STATUS_CODE_MESSAGES = {
    "UNASSIGNED" : "The job is unassigned.",
    "ASSIGNED" : "The job has been assigned to a device.",
    "FAILED" : "The job has failed.",
    "SUCCEEDED" : "The job has succeeded!"
}

###----- Helper Functions -----###
def get_job_status(job_id):
    resp = requests.get(f"{SERVER_ENDPOINT}/jobs/{job_id}/status/").json()
    return resp
class MapReduce():
    def __init__(self,mapper_file,reducer_file,n_machines,chunks,timeout):
        #todo actually deal with the number of machines
        #chunks is a dict of the form chunk_id : chunk location
        self.mapper = mapper_file
        self.reducer = reducer_file
        self.n_machines = n_machines
        self.chunks = chunks
        self.mappers_todo = set(chunks.keys())
        self.reducers_todo = set()
        self.timeout = timeout

    def checker(self,job_id,chunk_id):
        job_status_code = None    
        t_end = time.time() + 600 #edit to be programmatic
        while time.time() < t_end:
            try:
                resp = get_job_status(job_id)
                new_job_status_code = resp['status_code']
                if new_job_status_code != job_status_code:
                    if new_job_status_code in ("UNASSIGNED", "ASSIGNED"):
                        pass
                    elif new_job_status_code == "FAILED":
                        pass
                    else:
                        self.mapper_success(resp,chunk_id)
                        print(f'{chunk_id}: {new_job_status_code}')
                        break
                    job_status_code = new_job_status_code
                    time.sleep(JOB_STATUS_POLL_INTERVAL_SECS)
            except (KeyboardInterrupt, SystemExit):
                break
    def mapper_success(self,response_message,chunk_id):
        # the job has succeeded
        print('in mapper success')
        outfile = f"chunk{chunk_id}.txt"
        with open(outfile,'w+') as f:
            #print(f'writing to {chunk_id}')
            #print(response_message['result'])
            try:
                f.write(response_message['result'])
            except(e):
                print(f'Error Writing: {e}')
        #mr_db.put_in_db(outfile)
        print(f'discarding {chunk_id}')
        self.mappers_todo.discard(chunk_id)        
    def submit_job(self,zipf,chunk_id):
        """zipfile points to the zipfile that contains the code"""
        cpus = -1
        memory_mb = -1
        max_runtime_secs = 120 #make programma
        contents = []
        z = zipfile.ZipFile(zipf, "r")
        for filename in z.namelist(  ):
            as_bytes = z.read(filename)
            contents.append({"filename": filename, "bytes": as_bytes})
        job_spec = {
            "code_url": "",
            "contents": contents,
            "persist": 0,
            "resource_requirements" : {
                "cpus" : cpus,
                "memory_mb" : memory_mb,
                "max_runtime_secs" : max_runtime_secs
            }
        }
        print ("Submitting job...")
        res = requests.post(submit_job_url, json=job_spec)
        print ("Submitted")
        #if res.status_code != 200:
        #    print ("Could not submit job, returning..")
        #resp = res.json()
        #if not resp.get("job_id", False):
        #    print("No job ID returned, returning..")
        #    return            
        job_id = res.json()['job_id']
        print("Starting Checker")
        th = threading.Thread(target=self.checker,args=(job_id,chunk_id))
        th.start()

    def init_mapper(self,chunk,chunk_id):
        print("Initializing mapper for chunk ID"+str(chunk_id))     
        os.system("mkdir main")
        os.system("mkdir main/main")        
        os.system("cp template_main/* main/main")
        os.system(f"cp chunks/{chunk} main/main/chunk.txt")
        os.system(f"cp {self.mapper} main/main/mapfunc.py")
        shutil.make_archive('main', 'zip', 'main')
        self.submit_job(f"main.zip",chunk_id)
        os.system("rm -rf main")
        os.system("rm main.zip")
    def init_reducer(self,key):
        pass
    def get_keys(self):
        #this will grab all of the keys from the db
        pass
    def logger(self):
        while True:
            time.sleep(1)
            print(len(self.mappers_todo))
    def run(self,level):
        #init the logger
        #thc = threading.Thread(target=self.logger)
        #thc.start()
        #asynchronously spin up the mappers
        for (chunk_id,chunk) in self.chunks.items():
            self.init_mapper(chunk,chunk_id)
            #time.sleep(0.1)
        #wait for the mappers to complete
        while len(self.mappers_todo) > 0:
            pass
        print("HERE")
        if level=='all':
            pass
            #get all of the keys from the db
            #keys = self.get_keys()
            #asynchronously spin up the reducers
            #for key in keys:
            #    self.init_reducer(key)
        #thc.join()
    
