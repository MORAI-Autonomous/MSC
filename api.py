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
        api.launcher_start()   

    def signal_handler(self, signal, frame):        
        sys.exit(0)                                           

if __name__ == "__main__":
    start=api()
    
