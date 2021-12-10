import requests
import time
import threading
import sys

HEARTBEAT_INTERVAL_SECS = 0.33
#SERVER_ENDPOINT = "http://localhost:5000"
SERVER_ENDPOINT = "http://192.168.1.65:5000"

# get the device id (should already exist on the phone)
with open("./id.txt", "r") as f:
    device_id = int(f.readline())

def register_device():
    url = f"{SERVER_ENDPOINT}/devices/register/"
    # hardcode the params for now
    params = {
        "timestamp" : time.ctime(),
        "smart_plug_key": "key",
        "id" : device_id
    }
    resp = requests.post(url, json = params)
    resp_json = resp.json()
    if resp.status_code == 400 and resp_json['error_code'] == "DEVICE_ALREADY_REGISTERED":
        # device is already registered, this is a benign error
        print ("This device is already registered")
    else:
        assert resp.status_code == 200, "Device registration failed! " + str(resp_json)

def send_heartbeat():
    '''
    result = subprocess.Popen(["upower"], stdout = subprocess.PIPE)
    output = (result.communicate())
    '''
    # hardcode the params for now
    params = {
        "timestamp" : time.ctime(),
        "system" : {
            "cpu" : 0.6,
            "battery": 0.82,
        }
    }
    #util.cpu_use(),
    #        "battery": util.battery_level(),
    #        "disk": util.disk_use(),
    #        "pluggedin": util.plugged_in()
    url = f"{SERVER_ENDPOINT}/devices/{device_id}/heartbeat/"
    resp = requests.post(url, json = params)
    resp_json = resp.json()
    if resp.status_code == 400 and resp_json['error_code'] == "DEVICE_NOT_FOUND":
        # The device was not found, so register the device and retry the heartbeat
        register_device()
        resp = requests.post(url, json = params)

    assert resp.status_code == 200, "Device heartbeat failed!"
    
    # send a heartbeat every `HEARTBEAT_INTERVAL_SECS` seconds
    threading.Timer(HEARTBEAT_INTERVAL_SECS, send_heartbeat).start()

register_device()
send_heartbeat()
