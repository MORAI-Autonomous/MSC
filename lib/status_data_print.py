#!/usr/bin/env python
# -*- Encoding: utf-8 -*-

from lib.define import * 

"""
새로운 
platform, stage, status, command 등
새로운 데이터 추가 시 Define.py 정의 하고,
적절한 dict에 추가만 해주면 사용가능.
"""

class status_parser:
    def __init__(self):
        self.status_dict = {            
            #LAUNCHER
            '0x01' : {
                'platform' : 'Launcher',                
                '0x01' : { #BEFORE LOGIN
                    'stage'  : '로그인 전 상태',      
                    #LAUNCHER  BEFORE LOGIN STATUS              
                    '0x0001' : { 'status' : '대기상태' }
                },                              
                '0x02' : { #AFTER LOGIN
                    'stage'  : '로그인 후 상태',
                    #LAUNCHER AFTER LOGIN STATUS
                    '0x0001' : { 'status' : '시뮬레이터 버전 선택 됨' },
                    '0x0002' : { 'status' : '시뮬레이터 버전 선택 안됨' },
                    '0x0003' : { 'status' : '시뮬레이터 설치 필요 상태' },
                    '0x0004' : { 'status' : '에셋번들 다운로드 중' },
                    '0x0005' : { 'status' : '시뮬레이터 다운로드 중' },
                    '0x0006' : { 'status' : '로그인 완료 상태' },
                    '0x0007' : { 'status' : '시뮬레이터 종료 후 런쳐 대기상태' }
                },
                #LAUNCHER COMMAND                
                '0x0000' : { 'command' : '명령없음' },
                '0x0001' : { 'command' : '로그인 명령' },
                '0x0002' : { 'command' : '시뮬레이터 선택 명령' },
                '0x0003' : { 'command' : '시뮬레이터 설치 명령' },
                '0x0004' : { 'command' : '시뮬레이터 실행 명령' },
                '0x1000' : { 'command' : '런처 종료 명령' },
                '0x1001' : { 'command' : '런처 로그아웃' }
            },                          
            #Simulator
            '0x02' : {
                'platform' : 'Simulator',
                '0x01' : {#LOBBY
                    'stage'  : '로비 진입 상태',
                    #SIMULATOR LOBBY STATUS
                    '0x0001' : { 'status' : '대기상태' },
                    '0x0002' : { 'status' : '맵/차량 선택 안됨' },
                    '0x0003' : { 'status' : '로딩중' }
                },
                '0x02' : {#PLAY
                    'stage'  : '플레이 상태',
                    #SIMULATOR PLAY STATUS
                    '0x0001' : { 'status' : '대기 상태(플레이 상태)' },
                    '0x0002' : { 'status' : '시뮬레이션 정지 상태' },
                    '0x0003' : { 'status' : '로딩중' },
                    '0x0004' : { 'status' : '종료 명령으로 인한 시뮬레이션 종료 중' },
                    '0x0005' : { 'status' : '맵 변경이 완료' }
                },           
                #SIMULATOR COMMAND
                '0x0000' : { 'command' : '명령없음' },
                '0x0001' : { 'command' : '시뮬레이션/옵션 변경 실행 명령' },
                '0x0002' : { 'command' : '시뮬레이션 Pause' },
                '0x0003' : { 'command' : '시뮬레이션 Play' },
                '0x0011' : { 'command' : '네트워크 데이터 세팅 명령' },
                '0x0012' : { 'command' : '센서 데이터 세팅 명령' },
                '0x0013' : { 'command' : '시나리오 데이터 세팅 명령' },
                '0x0014' : { 'command' : '시나리오 데이터 저장 명령' },
                '0x0015' : { 'command' : '센서 데이터 저장 명령' },
                '0x0016' : { 'command' : '네트워크 데이터 저장 명령' },
                '0x1000' : { 'command' : '시뮬레이터 종료 명령' }
            },  
            #Option result
            'result' : {
                '0x00' : '명령 없음',
                '0x01' : '성공',
                '0x11' : '유효하지 않은 플랫폼',
                '0x12' : '유효하지 않은 스테이지',
                '0x23' : 'ID 오류',
                '0x24' : 'PW 오류',
                '0x25' : '시뮬레이터 버전 오류',
                '0x26' : '시뮬레이터 설치 안됨',
                '0x31' : '유효하지 않은 맵 옵션',
                '0x32' : '유효하지 않은 차량 옵션',
                '0x33' : '네트워크 로드 오류(유요한 파일 이름이 없을때)',
                '0x34' : '네트워크 로드 오류(파일은 있지만 초기화 실패)',
                '0x35' : '센서 로드 오류(유효한 파일 이름이 없을때)',
                '0x36' : '센서 로드 오류(파일은 있지만 초기화 실패)',
                '0x37' : '시나리오 로드 오류'
            }
        }        

    
    def print_info(self,status_data):        
        try:            
            platform, stage, status, cmd_platform, cmd, cmd_option, result = status_data
            is_wait = '0x1000'
            print(platform, stage, status, cmd_platform, cmd, cmd_option, result)
            print_platform = self.status_dict[platform]['platform']
            print_stage = self.status_dict[platform][stage]['stage']         
            if int(is_wait, 16) < int(status, 16):
                print_status = 'Wait_status'  
            else:
                print_status = self.status_dict[platform][stage][status]['status']

            print(f'Data_Platform = {print_platform}')  
            print(f'Data_Stage = {print_stage}')
            print(f'Data_Status = {print_status}')

            #--- Command print ---#
            if not cmd == '0x0000':
                print_cmd_platform = self.status_dict[cmd_platform]['platform']
                print_cmd_command = self.status_dict[cmd_platform][cmd]['command']                
                print_cmd_result = self.status_dict['result'][result]
                print_cmd_option = cmd_option
                
                print(f'Command_Platform = {print_cmd_platform}')
                print(f'Command_Cmd = {print_cmd_command}')                                
                print(f'Command_Option = {print_cmd_option}')               
                print(f'Command_Result = {print_cmd_result}')
            
            print('-------------(22.06.16)')
            
        except :
            pass