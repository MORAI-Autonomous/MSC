#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time,os
from lib.define import *
from lib.read_text import *
from lib.controller import *

class launcher_start(controller):

    def __init__(self):
        self.controller = controller()

    def launcher_start(self):

        while True:
            if self.controller.update(): #data update
                
                self.controller.is_downloading() #check downloading status

                if self.controller.is_befor_login():
                    self.controller.commander(Command.LOGIN, f'{user_id}/{user_pw}')#Login명령
                        
                if self.controller.is_after_login() or self.controller.is_after_sim_quit_to_launcher():  # is_after_sim_quit_to_launcher : Simulator에서 quit 명령 후 Launcher 복귀 상태 확인
                                        
                    if not self.controller.is_version_selected():
                        self.controller.commander(Command.SELECT_VER, version)#version 선택명령
                        
                        if self.controller.is_not_find_version(): #선택한 버전이 없는 버전인지 확인.                    
                            break
                    
                    if self.controller.is_can_execute_sim():
                        self.controller.commander(Command.EXECUTE_SIM,'') #Simulator 실행 명령
                                                
                    if self.controller.is_sim_not_install():
                        self.controller.commander(Command.INSTALL_SIM,'') #Simulator 설치 명령

                if self.controller.is_sim_lobby():
                    self.controller.commander(Command.MAP_VEHICLE_SELECT, f'{map}/{vehicle}')#시뮬레이션/옵션 변경 실행 명령

                if self.controller.is_sim_playing():
                    if network_file :
                        self.controller.commander(Command.NET_SETTING, network_file) #시뮬레이터 네트워크 세팅 명령
                    if sensor_file:
                        self.controller.commander(Command.SEN_SETTING, sensor_file) #시뮬레이터 센서 세팅 명령
                    if scenario_file:
                        self.controller.commander(Command.SCEN_SETTING, f'{scenario_file}/30') #시뮬레이터 시나리오 세팅 명령
                    '''
                        Scenario Setting Option
                        0x01 : Delete All
                        0x02 : Ego Vehicle
                        0x04 : Surround Vehicle
                        0x08 : Pedestrian
                        0x10 : Obstacle
                        0x20 : Pause (scenario load 후 시뮬레이터 정지(직접 esc키 또는 play command로 해제 가능))
                        원하는 option을 or 연산 해서 사용
                        e.g) Ego vihcle  Surrond Vehicle, Pedestrain, Obstacle을 load하려면
                             0x02 | 0x04 | 0x08 | 0x10  -> 0b0010 | 0b0100 | 0b1000 | 0b0001 0000 -> 30 (0b0001 1110, 0x1E)
                    '''
                    break

            else :                
                print("[NO Simulator Control Data]",end='\r')                