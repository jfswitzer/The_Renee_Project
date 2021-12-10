import requests

def power_on(key):
    print("Power On Command Sent")
    requests.get("https://maker.ifttt.com/trigger/battery_low/with/key/" + key)

def power_off(key):
    print("Power Off Command Sent")
    requests.get("https://maker.ifttt.com/trigger/battery_high/with/key/" + key)