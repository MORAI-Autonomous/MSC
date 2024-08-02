#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os, signal
from lib.controller import *
from lib.launcher_start_api import *
from lib.read_text import *
"""
https://docs.google.com/spreadsheets/d/1jHbR_JoZFYfxMirwSp-48peWkJf1xUmMZyFIwetxcZM/edit#gid=0

"""


class api :

    def __init__(self):         

        signal.signal(signal.SIGINT, self.signal_handler) #handle ctrl-c
        
        api = launcher_start()
        api.controller.update()
        #api.launcher_start()

        #LAUNCHER COMMAND

        #Login
        ID = '' # e.g) user1
        PW = '' # e.g) 1234
        api.controller.commander(Command.LOGIN,ID+'/'+PW)

        #Simualtor version select
        verson = ''# v.4.7.211109.H3
        api.controller.commander(Command.SELECT_VER,version)

        #Simualtor install
        api.controller.commander(Command.INSTALL_SIM,'')

        #Simaltor exectue
        api.controller.commander(Command.EXECUTE_SIM,'')

        #Launcher exit
        api.controller.commander(Command.QUIT_LAUNCHER,'')

        #Launcher logout
        api.controller.commander(Command.LOGOUT,'')

        
        
        
        #SIMULATOR COMMAND

        #Simulator option change(map/vehicle)
        _map : '' #e.g) R_KR_PG_K-City
        vehicle : '' #e.g) 2017_Kia_Niro(HEV)
        api.controller.commander(Command.MAP_VEHICLE_SELECT,_map+'/'+vehicle)

        #Simaultor play
        api.controller.commander(Command.SIM_PLAY,'')

        #Simaultor play
        api.controller.commander(Command.SIM_PAUSE,'')

        #Simaultor Network Setting
        network_file = ''
        api.controller.commander(Command.NET_SETTING,network_file)

        #Simaultor Network Save
        network_file = ''
        api.controller.commander(Command.NET_SAVE,network_file)

        #Simaultor Sensor Setting
        sensor_file = ''                
        api.controller.commander(Command.SEN_SETTING,sensor_file)

        #Simaultor Sensor Save
        sensor_file = ''                
        api.controller.commander(Command.SEN_SAVE,sensor_file)

        #Simaultor Scenario Setting
        scenario_file = ''
        api.controller.commander(Command.SCEN_SETTING,scenario_file)

        #Simaultor Scenario save
        scenario_file = ''
        api.controller.commander(Command.SCEN_SAVE,scenario_file)

        #Simualtor exit
        api.controller.commander(Command.QUIT_SIM,'')

    


    def signal_handler(self, signal, frame):        
        sys.exit(0)                                           

if __name__ == "__main__":
    start=api()
    
