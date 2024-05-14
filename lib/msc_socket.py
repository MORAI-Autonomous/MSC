#!/usr/bin/env python
# -*- Encoding: utf-8 -*-


from lib.udp_parser import udp_parser, udp_sender
from lib.read_text import *

class msc_socket:
    def __init__(self):
        #udp_parser, udp_sender 생성
        self.get_status = udp_parser(recive_user_ip, recive_user_port,'get_sim_status')        
        self.set_status = udp_sender(request_dst_ip, request_dst_port,'set_sim_status') 
        print("socket")

    def connect(self):
        return self.get_status, self.set_status