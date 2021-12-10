# eventlet must be called very very early (before Flask) so I can use it to do chron jobs with socketio
# without eventlet = alot of issues with the packet not sending over to the client and issues 
# of recursion depth exceeding limits.
import eventlet
eventlet.monkey_patch()

from datetime import datetime

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = "actualsecret"
socketio = SocketIO(app)

import db

# For the Checker class
import threading
from datetime import timedelta
import time

# ============== BEGINNING OF CHECKER CODE ============== #
# Checker Chron
# 1. checks each job to see if they time out
# 2. if job times out, restart it
# 3. if job repeatedly fails, then stop it after 3 retries
# 4. if phone does not acknowledge task, increment its failed acks num

MAX_FAILS = 100 #max fails is for full decomissioning
CHECK_JOBS_INTERVAL_SEC = 0.1 #check for jobs that need to be scheduled
ACK_TIMEOUT = 3 #no ack for 3s, time out 
class Checker:

    def __init__(self):
        self.stopped = False
        self.pending_job_acks = {}

    def check_jobs(self):
        if self.stopped:
            # stops recursively generating threads.
            return
        while not self.stopped:
            #print("[CHECKING JOBS]")
            jobs = db.get_all_jobs()

            # ==== for each job ====
            for job in jobs:
                job_json = job.to_json()
                job_max_secs = job_json["resource_requirements"]["max_runtime_secs"]

                # Check if job timed out, if so then try to cancel it and reschedule it.
                if job_max_secs > 0 and job_json["status"] == job.ASSIGNED and job_json["assigned_device_id"] is not None:
                    time_updated = datetime.strptime(job_json["time_updated"], '%Y-%m-%d %H:%M:%S.%f')
                    timeout_datetime = timedelta(seconds = job_max_secs) + time_updated
                    if timeout_datetime < datetime.utcnow():

                        # update device's num_failed_jobs
                        device = db.get_device(job_json["assigned_device_id"])
                        device.num_failed_jobs += 1
                        device.save()

                        print("[JOB TIMEOUT]: Device", device.id, "on Job", job.id)

                        self.cancel_and_reschedule_job(job.id)


                # For unassigned jobs.
                if job_json["status"] == job.UNASSIGNED:
                    # Check if the phone has not acknowledged the job for 10 seconds. If so, then increase the num_failed_acks and reschedule the job
                    time_updated = datetime.strptime(job_json["time_updated"], '%Y-%m-%d %H:%M:%S.%f')
                    timeout_datetime = timedelta(seconds = ACK_TIMEOUT) + time_updated
                    if timeout_datetime < datetime.utcnow() and job.id in self.pending_job_acks:

                        # update device's num_failed_acks
                        device = db.get_device(self.pending_job_acks[job.id])
                        device.num_failed_acks += 1
                        device.save()

                        print("[NO DEVICE ACK]: Device", device.id, "on Job", job.id)

                        self.remove_pending_acknowledgement(job.id)
                        self.cancel_and_reschedule_job(job.id)

                    # For jobs that are just unassigned in general, hence there is no pending ack's:
                    elif job.id not in self.pending_job_acks and job.can_be_retried:
                        schedule_job(job)

                # For failed jobs: retry them.
                if job_json["status"] == job.FAILED and job.can_be_retried:
                    schedule_job(job)


            # ==== END of "for each job" section ====

            # Start another thread in a few seconds
            # threading.Timer(CHECK_JOBS_INTERVAL_SEC, self.check_jobs).start()
            time.sleep(CHECK_JOBS_INTERVAL_SEC)


    def check_phones(self):
        if self.stopped:
            # stops recursively generating threads.
            return

        while not self.stopped:
            #print("[CHECKING PHONES]")

            # ==== Check devices' num failed counts ====
            for device in db.get_all_devices():

                # ==== If the device has failed too many times, decommission it ==== #
                if device.num_failed_acks + device.num_failed_jobs > MAX_FAILS and not device.decommissioned:
                    device.stop_charging()
                    device.decommission()
                    print(f"[DEVICE {device.id}] DECOMMISSIONED.")
            time.sleep(1)


    def stop(self):
        self.stopped = True

    def add_pending_acknowledgement(self, job_id, device_id):
        self.pending_job_acks[job_id] = device_id

    def remove_pending_acknowledgement(self, job_id):
        if job_id in self.pending_job_acks:
            del self.pending_job_acks[job_id]

    def cancel_and_reschedule_job(self, job_id):
        job = db.get_job(job_id)
        job_json = job.to_json()

        # cancel the job
        job.cancel()

        print(f"[JOB {job.id}] cancelled and rescheduled.")

        # Reschedule the job for another device, if and only if the number of retries don't go past 3.
        if job.can_be_retried:
            if(schedule_job(job)):
                print(f"[JOB {job.id}] Rescheduled")
        else:
            print(f"[JOB {job.id}] Reschedule Limit Hit")

checker = Checker()

eventlet.spawn(checker.check_jobs)
eventlet.spawn(checker.check_phones)

def schedule_job(job):
    device_id = db.schedule_job(job)
    if device_id is None:
        print("[NO DEVICES AVAILABLE]")
        return False

    # used to make sure that the phone eventually acknowledges it, if not then we reschedule the job
    checker.add_pending_acknowledgement(job.id, device_id)
    return True


# ============== END OF CHECKER CODE ============== #


# TODO: Flesh out all API code to properly format and return errors as json responses
@app.route('/devices/register/', methods=['POST'])
def register_device():
    metadata = request.get_json()
    device_id = metadata.pop('id')

    if device_id is None:
        return jsonify(success=False, error_code="MISSING_DEVICE_ID"), 400

    if not isinstance(device_id, int):
        return jsonify(success=False, error_code="DEVICE_ID_NOT_AN_INTEGER"), 400

    # check if the device is already registered
    if db.get_device(device_id=device_id):
        return jsonify(success=False, error_code="DEVICE_ALREADY_REGISTERED"), 400

    smart_plug_key = metadata.pop("smart_plug_key")
    if not smart_plug_key:
        return jsonify(success=False, error_code="MISSING_DEVICE_SMART_PLUG_KEY"), 400

    db.create_device(device_id=device_id, smart_plug_key=smart_plug_key, metadata=metadata)
    return jsonify(success=True, device_id=device_id)


@app.route("/devices/<int:device_id>/heartbeat/", methods=['POST'])
def device_heartbeat(device_id):
    device = db.get_device(device_id=device_id)
    if not device:
        return jsonify(success=False, error_code="DEVICE_NOT_FOUND"), 400

    # metadata stores a json object of arbitrary device related data (such as battery life, cpu mem, etc.)
    device.metadata = request.get_json()
    device.update_metadata_history()

    device.last_heartbeat = datetime.utcnow()
    device.save()

    # TODO: need to add charging logic based on phone's battery level on heartbeat
    # possibly something like phone.metadata.charge < 20 -> phone.start_charging() ...
    #if device.needs_to_start_charging() and not device.decommissioned:
    #    device.start_charging()
    #elif device.needs_to_stop_charging() and not device.decommissioned:
    #    device.stop_charging()
    #elif device.decommissioned: # if the device is behaving badly, stop charging it.
    #    device.stop_charging() 

    return jsonify(success=True)

@app.route("/devices/")
def devices_list():
    return jsonify(success=True, devices=[device.to_json() for device in db.get_all_devices()])

@app.route("/jobs/")
def jobs_list():
    return jsonify(success=True, jobs=[job.to_json() for job in db.get_all_jobs()])

@app.route("/jobs/submit/", methods=['POST'])
def job_submit():
    body = request.get_json()
    assert "resource_requirements" in body
    assert "code_url" in body

    job = db.create_job(job_spec=body)

    job_schedule_success = schedule_job(job)
    if not job_schedule_success:
        return jsonify(success=False, error_code="NO_DEVICES_ARE_AVAILABLE"), 500

    return jsonify(success=True, job_id=job.id)

@app.route("/jobs/<int:job_id>/status/")
def job_status(job_id):
    job = db.get_job(job_id)
    if not job:
        return jsonify(success=False, error_code="INVALID_JOB_ID"), 400

    status_code = db.Job.STATUS_CODES[job.status]
    return jsonify(success=True, status_code=status_code)

@app.route("/jobs/<int:job_id>/update_status/", methods=['POST'])
def job_update_status(job_id):
    body = request.get_json()

    assert "device_id" in body
    assert "status" in body

    device_id = body['device_id']
    status = body['status']

    result = body.get("result")

    device = db.get_device(device_id)
    if not device:
        return jsonify(success=False, error_code="INVALID_DEVICE_ID"), 400

    job = db.get_job(job_id)
    if not job:
        return jsonify(success=False, error_code="INVALID_JOB_ID"), 400

    if not job.assigned_device:
        return jsonify(success=False, error_code="CANNOT_UPDATE_UNASSIGNED_JOB")

    if job.assigned_device.id != device_id:
        return jsonify(success=False, error_code="JOB_ASSIGNED_TO_ANOTHER_DEVICE"), 400

    job.status = status

    if status == db.Job.SUCCEEDED or status == db.Job.FAILED:
        # This job has finished, so it's no longer assigned to a device
        job.assigned_device = None

        if result:
            print(f"\n\n[JOB RESULT] Received output for job id {job_id}:")
            print(result, "\n\n")

    job.save()
    return jsonify(success=True)

@app.before_request
def before_request():
    db.db.connect(reuse_if_open=True)

@app.after_request
def after_request(response):
    db.db.close()
    return response

'''
Socket IO events:
 - connect
 - disconnect
 - receive ACK from phones
'''
@socketio.on('connect')
def test_connect():
    device_id = request.args.get("device_id", type=int)
    device = db.get_device(device_id=device_id)
    if device_id==20:
        print ("Lambda server connected")    
    if not device and (device_id != 20):
        # Unknown device tried to connect
        print ("Rejecting unknown device connection")
        return False
    print(f"Device id={device_id} has connected")

@socketio.on('disconnect')
def test_disconnect():
    print('A device has disconnected')

@socketio.on('cancel_job')
def handle_phone_cancel_job_response(data):
    success = data['success']
    device_id = data['device_id']
    job_id = data['job_id']

    if success:
        # the phone was able to stop this job
        job = db.get_job(job_id=job_id)
        job.status = db.Job.FAILED
        job.assigned_device = None
        job.save()
        print (f"Device id={device_id} was able to cancel job id={job_id}")
    else:
        # the phone could not cancel this job
        # in this case, we don't do anything on this part of the SERVER side, since we should have a separate server cron process that handles failed jobs
        # (e.g., picks such failed jobs up and retry them if needed)
        # the device, however, would need to somehow end this task.
        print (f"Device id={device_id} was NOT able to cancel job id={job_id}")

@socketio.on('task_acknowledgement')
def handle_phone_response(data):
    device_id = data['device_id']
    job_id = data['job_id']

    job = db.get_job(job_id=job_id)
    job.status = db.Job.ASSIGNED
    job.assigned_device = device_id
    job.num_attempts += 1
    job.save()

    checker.remove_pending_acknowledgement(job.id)

    print (f"Device id={device_id} has acknowledged job id={job_id}")


if __name__ == '__main__':
    # app.run(host="0.0.0.0")
    socketio.run(app, host='0.0.0.0', debug=False)
    # socketio.run(app, host='0.0.0.0', debug=True)
