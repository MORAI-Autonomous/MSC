#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
import os 
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'params.txt')
file = open(file_path, 'r')
line = file.read()
params = line.split('\n')

for index, data in enumerate(params):        
    try:
        if params[index].find('\r'): #Linux
            params[index] = data.split(':')[1].replace(" ","").replace("\r","")
        else:
            params[index] = data.split(':')[1].replace(" ","")
    except Exception as e :     
        print(e)
        pass

recive_user_ip = params[0].strip()
recive_user_port = int(params[1].strip())
request_dst_ip = params[2].strip()
request_dst_port = int(params[3].strip())
user_id = params[4].strip()
user_pw = params[5].strip()
version = params[6].strip()
map = params[7].strip()
vehicle = params[8].strip()
if len(params[9].strip()) == 0 :
    network_file = None
else:
    network_file = params[9].strip()

if len(params[10].strip()) == 0 :
    sensor_file = None
else:
    sensor_file = params[10].strip()
    
if len(params[11].strip()) == 0 :
    scenario_file = None
else:
    scenario_file = params[11].strip()        