#!/usr/bin/env python
# -*- Encoding: utf-8 -*-
import time, os, platform
from lib.udp_parser import udp_parser, udp_sender
from lib.define import *
from lib.msc_socket import msc_socket
from lib.status_data_print import *

class controller(msc_socket):

    def __init__(self):
        super(controller,self).__init__()        
        self.status_data = None
        self._ing = False
        
    #Launcher, simulator에서 보내주는 데이터 update
    def update(self):        
        time.sleep(0.5)
        self.status_data = self.get_status.get_data()
        if len(self.status_data) == 0:
            return False
        else:
            self.platform, self.stage, self.status, self.cmd_platform, self.cmd, self.cmd_option, self.result = self.status_data
            self.clear()
            status_parser.print_info(status_parser(),self.status_data)

            #_ing status pass 
            if not self._ing:                
                self.is_downloading()
            return True

    #Launcher, simulator로 명령 전송
    def commander(self,cmd,option):#change_option
        cmd_platform, cmd_command, cmd_option = Command_list[cmd].value
        
        if self.platform == cmd_platform : 
            #Option이 필요없는 명령은 self.custom_option=''으로 처리.
            if cmd == Command.INSTALL_SIM or cmd == Command.EXECUTE_SIM or cmd == Command.QUIT_LAUNCHER or cmd == Command.LOGOUT or cmd == Command.SIM_PLAY or cmd == Command.SIM_PAUSE or cmd == Command.QUIT_SIM:            
                custom_option = cmd_option #cmd_option == ''            
            else:
                custom_option = option                    
            self.send_data(cmd_platform,cmd_command,custom_option) 
            
            self.update()
            self.is_waitting()
        else:
            print('!!!Do not send other paltfrom command!!!')
            print(f'current_platform : {self.platform}, command_platform : {cmd_platform}')
            

    #Launcher platform에서 시뮬레이터 실행하기 전 verison을 선택해야 하는데, 이 때 선택한 버전에대해 체크(아마도 params.txt에 버전 오타일 가능성.)
    def is_not_find_version(self):        
        if self.result == Result.ERROR_VERSION:
            print("Please check simulation version")

        return self.result == Result.ERROR_VERSION

    #Launcher platform에서 로그인 전 상태                    
    def is_befor_login(self):
        return self.platform == Platform.LUANCHER and self.stage == Stage.BEFORE_LOGIN 

    #Launcher platform에서 로그인 후 상태(stage, status)
    def is_after_login(self):
        return self.platform == Platform.LUANCHER and self.stage == Stage.AFTER_LOGIN

    def is_version_selected(self):
        return self.platform == Platform.LUANCHER and self.stage == Stage.AFTER_LOGIN and self.status == Status.VER_SELECTED

    #Launcher Platform에서 simulator가 설치 되어 있지 않은 상태.
    def is_sim_not_install(self):
        return self.platform == Platform.LUANCHER and self.status == Status.NEED_INSTALL and self.result == Result.NOT_INSTALL

    #Launcher Platform에서 시뮬레이터 실행 가능 상태(버전 선택 됨)
    #원하는 버전 선택 시 설치되어있지 않으면 morai_launcher에서 is_sim_not_install 의 상태를 보내준다.
    def is_can_execute_sim(self):
        return self.platform == Platform.LUANCHER and self.status == Status.VER_SELECTED and self.result == Result.SUCCESS

    #Launcher Platform에서 시뮬레이터 종료 후 상태
    def is_after_sim_quit_to_launcher(self):
        return self.platform == Platform.LUANCHER and self.status == Status.QUIT_SIM_SUCCESS 

    #Simualtor 실행이 완료 될 때까지 대기
    def watting_execute(self):
        count = 0        
        while True:     
            try:   
                #data _update
                self.update()
                print(f'exe_loading{"."*count}')
                if count == 5 :
                    count = 0
                count += 1 
                
                #Simualtor platform의 hoding(대기) 상태이면 while break
                if self.platform == Platform.SIMULATOR and self.status == Status.HOLDING:
                    break
            except KeyboardInterrupt:
                break

    #Simualtor의 로비 상태 (맵/ 차량 선택 화면)
    def is_sim_lobby(self):
        return self.platform == Platform.SIMULATOR and self.stage == Stage.LOBBY and self.status == Status.HOLDING #Simulator platform에서 로비 Stage의 대기상태

    #Simualtor의 플레이 상태 (맵/ 차량 로딩 완료)
    def is_sim_playing(self):
        return self.platform == Platform.SIMULATOR and self.stage==Stage.PLAY and (self.status==Status.MAP_OK or self.status == Status.HOLDING)#simulator map/vehicle 로딩 완료
                                                                                   

    
    #Simulator 실행에 필요한 파일 다운로드 상태
    def is_downloading(self):        
        if self.platform == Platform.LUANCHER and (self.status == Status.SIM_DOWNLOADING or self.status == Status.ASSET_DOWNLOADING):           
            count = 0
            while True:                    
                self._ing = True
                print(f'Downloading{"."*count}')
                self.update()

                if count == 5 :
                    count = 0                    
                count += 1

                if not (self.status == Status.ASSET_DOWNLOADING or self.status == Status.SIM_DOWNLOADING):
                    self._ing = False
                    break

    #scripts에서 보낸 명령에 대해서 Launcher, Simulator가 처리를 완료 할 때까지 watting
    #기본적으로 0x0001의 상태에 대해 처리를 시작하면 Launcher, simualtor에서 0x1001이라는 status를 보내주고
    #처리가 완료되면 다시 is_wait값인 0x1000이 빠진 0x0001값을 받을 수 있다.     
    def is_waitting(self):
        self.is_wait = '0x1000'       
        if int(self.is_wait,16) < int(self.status,16):       
            self._ing = True
            count = 0            
            while True:              
                self.update()   
                print(f'Waitting{"."*count}')
                if count == 5:
                    count = 0
                count += 1

                if int(self.status,16) < int(self.is_wait,16):
                    self._ing = False
                    break


    def send_data(self, cmd_platform, cmd_command, cmd_option):

        try:
            print(f'send>>{cmd_platform,cmd_command,cmd_option}')
            cmd_platform = int(cmd_platform, 0)
            cmd_command = int(cmd_command, 0)
            cmd_option = cmd_option
            self.set_status.send_data([cmd_platform, cmd_command, cmd_option])
            time.sleep(0.5)
            
        except ValueError:
            print("Invalid input")    


    def clear(self):
        operation = platform.system()
        if operation == "Linux":
            os.system("clear")
        elif operation == "Windows":
            os.system("cls")        