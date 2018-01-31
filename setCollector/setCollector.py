#!/opt/zenoss/bin/zendmd

'''
This script is used to move zenoss monitored devices from its\' current collector to a new collector
The configuration file "setCollector.json" needs to be under same foloder of the script.
'''

import json
import sys


TARGET = ''
MOVEDATA = True
DEVICENAMELIST = []
DEVICES_TO_MOVE = []

with open ("setCollector.json") as conf:
    conf_data = json.load(conf)
    TARGET = conf_data["target"]
    MOVEDATA = conf_data["moveData"]
    for device_name in conf_data["devices"]:
        DEVICENAMELIST.append(device_name)

# Check if TARGET is an valid collector
collectors = []
for hubObj in dmd.Monitors.Hub.getHubs():
    for collectorObj in hubObj.collectors():
        collectors.append(collectorObj.id)
if TARGET not in collectors:
    print "ERROR: collector " + TARGET + " doesn't exist, please verfiy" 
    sys.exit(-2)
df = getFacade('device')

# Check if all the Devices are valid
for device_name in DEVICENAMELIST:
    dev = find(device_name) 
    if dev:
        dev_name_to_move = dev.getPrimaryId()
        DEVICES_TO_MOVE.append(dev_name_to_move)
    else:
        print "ERROR: " + device_name + " not found in Zenoss, please check devices in the setCollector.json again"
        sys.exit(-1)

if len(DEVICES_TO_MOVE):
    df.setCollector(DEVICES_TO_MOVE, TARGET, moveData=MOVEDATA)
    commit()
