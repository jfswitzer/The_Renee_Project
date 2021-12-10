# Quickstart
## Install python dependencies for the server
```shell script
pip install -r requirements.txt
```

## Create the database
**Note:** Only the first time the server is run on a new Pi
```shell script
python create_db.py
```
After running this command, a `database.db` file should be created in the current folder (`pi_server`).

## Start the backend API server
```shell script
python app.py
```

## MVP workflow
### Register a new device
```shell script
cd ../phones # go to the phones/ folder
python send_heartbeat.py &
```

This script will register a new device with the server and will send heartbeat to the server every 60 seconds in the background. This script should be run from the phone.

### Open a socket
```shell script
cd ../phones # go to the phones/ folder
python client.py
```
This script will register a new device with the server and will open a real-time socket communication with the server. This script should be run form the phone.

### Submit a new task
```shell script
cd ../tests # go to the tests/ folder
python test_send_task.py
```

This script will submit a new task (with the job's code URL being `https://github.com/jfswitzer/ut_test.git`) to the Pi server.
Once this is done, go back to the terminal running the `test_socketio_phone.py` script process.
You should see this "device" receive the job, work on it (for 5 secs), and then update the server saying that the job has finished.

Be sure to checkout the `client.py` file's code to see the actual code/requests logic for receiving jobs and sending updates on the jobs (such as when they succeed/fail, etc.)

### View jobs and devices
At any point in this workflow, you can always view all devices and jobs with the following cURL commands:

#### Devices
```shell script
curl --location --request GET 'http://127.0.0.1:5000/devices/'
```

Example response:
```json
{
  "devices": [
    {
      "assigned_jobs": {
        "num_total": 0
      }, 
      "id": 1, 
      "last_heartbeat": "2021-05-04 00:40:19.647478", 
      "metadata": {}, 
      "smart_plug_key": "random_key", 
      "time_created": "2021-05-04 00:40:19.647330", 
      "time_updated": "2021-05-04 00:40:19.647498"
    }
  ], 
  "success": true
}
```

#### Jobs
```shell script
curl --location --request GET 'http://127.0.0.1:5000/jobs/'
```

Example response:
```json
{
  "jobs": [
    {
      "assigned_device_id": null, 
      "code_url": "https://github.com/jfswitzer/ut_test.git", 
      "id": 1, 
      "resource_requirements": {
        "cpus": -1, 
        "max_runtime_secs": -1, 
        "memory_mb": -1
      }, 
      "status": 3, 
      "num_attempts" : 1, 
      "can_be_retried" : false,
      "time_created": "2021-05-04 00:40:21.467057", 
      "time_updated": "2021-05-04 00:40:26.487776"
    }
  ], 
  "success": true
}
```

### Send a heartbeat
This would be sent from the phones to the server

```shell script
curl --location --request POST 'http://127.0.0.1:5000/devices/dev1/heartbeat/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "system" : {
        "cpu" : 0.8,
        "memory" : 16
    }
}'
```

Example response:
```json
{
    "success": true
}
```

## Setting up Wyze Smart Plug
1. Create a Wyze account and connect the smart plug to your account
2. Create a IFTTT account and connect your Wyze account to it
3. Create two IFTTT applets
    - Applet 1: If webhook with "battery_low" event, then turn on the smart plug.
    - Applet 2: If webhook with "battery_high" event, then turn off the smart plug.
4. Find your URL key: https://ifttt.com/maker_webhooks/ and click on Documentation.
5. Use your URL key to register the device through the pi_server