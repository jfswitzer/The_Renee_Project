import sys
import time
import pandas as pd
import requests, argparse
from halo import Halo

JOB_STATUS_POLL_INTERVAL_SECS = 5

SERVER_ENDPOINT = "http://192.168.1.30:5000"
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
def submit_job(code_url, cpus, memory_mb, max_runtime_secs):
    job_spec = {
        "code_url": code_url,

        # TODO: Later, when we add support for resource_requirements, test some real values for this
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Submit a list of jobs to our smartphone datacenter.')
    parser.add_argument('--jobs', help='The CSV file that contains the list of jobs', required=True)
    args = parser.parse_args()

    fn = args.jobs
    df = pd.read_csv(fn)
    for row in df.iterrows():
        row = row[1]
        submit_job(row['code_url'],row['cpus'],row['memory_mb'],row['max_runtime_secs'])

