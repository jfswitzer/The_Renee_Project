import sys
import time
import zipfile
import requests, argparse
import socketio
import threading
from halo import Halo

JOB_STATUS_POLL_INTERVAL_SECS = 0.1

#SERVER_ENDPOINT = "http://localhost:5000"
SERVER_ENDPOINT = "http://192.168.1.65:5000"
submit_job_url = f"{SERVER_ENDPOINT}/jobs/submit/"
    
def get_job_status(job_id):
    resp = requests.get(f"{SERVER_ENDPOINT}/jobs/{job_id}/status/").json()
    return resp['status_code']

#UNASSIGNED", "ASSIGNED", "FAILED", "SUCCEEDED
STATUS_CODE_MESSAGES = {
    "UNASSIGNED" : "The job is unassigned.",
    "ASSIGNED" : "The job has been assigned to a device.",
    "FAILED" : "The job has failed.",
    "SUCCEEDED" : "The job has succeeded!"
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Submit a job to our smartphone datacenter.')
    parser.add_argument('--code_url',default='',help='The github repo to run')
    parser.add_argument('--zipfile',default='',help='The zip folder to run')    
    parser.add_argument("--cpus", default=-1, help="The amount of CPUs required for the job")
    parser.add_argument("--memory_mb", default=-1, help="The amount of memory (MB) required for the job")
    parser.add_argument("--max_runtime_secs", default=30, help="The maximum runtime for this job (in seconds)")
    args = parser.parse_args()
    cpus = args.cpus
    memory_mb = args.memory_mb
    max_runtime_secs = args.max_runtime_secs
    code_url = args.code_url
    zipf = args.zipfile
    contents = []
    if code_url=='' and zipf=='':
        print("Please specify code url or zip file")
        sys.exit(1)
    elif zipf != '':
        z = zipfile.ZipFile(zipf, "r")
        for filename in z.namelist(  ):
            as_bytes = z.read(filename)
            contents.append({"filename": filename, "bytes": as_bytes})
    job_spec = {
        "code_url": code_url,
        "contents": contents,
        "resource_requirements" : {
            "cpus" : cpus,
            "memory_mb" : memory_mb,
            "max_runtime_secs" : max_runtime_secs
        }
    }
    print ("Submitting job...")
    res = requests.post(submit_job_url, json=job_spec)
    if res.status_code != 200:
        print ("Could not submit job!")
        sys.exit(1)

    resp = res.json()
    if not resp.get("success", False):
        print ("Could not submit job!")
        sys.exit(1)

    job_id = resp['job_id']

    job_status_code = None


    spinner = Halo(text="Waiting for job updates", spinner='dots')
    spinner.start()

    while True:
         try:
             new_job_status_code = get_job_status(job_id)
             if new_job_status_code != job_status_code:
                 if new_job_status_code in ("UNASSIGNED", "ASSIGNED"):
                     spinner.info(STATUS_CODE_MESSAGES[new_job_status_code])
                     spinner.start("Waiting for job updates")
                 elif new_job_status_code == "FAILED":
                     spinner.fail(STATUS_CODE_MESSAGES[new_job_status_code])
                     spinner.start("Waiting for job updates")
                 else:
                     # the job has succeeded
                     spinner.stop_and_persist(symbol='🦄'.encode('utf-8'), text=STATUS_CODE_MESSAGES[new_job_status_code])
                     break
                 job_status_code = new_job_status_code
                 time.sleep(JOB_STATUS_POLL_INTERVAL_SECS)
         except (KeyboardInterrupt, SystemExit):
             spinner.stop()
             break
