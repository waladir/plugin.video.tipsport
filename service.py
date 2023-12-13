# -*- coding: utf-8 -*-
import sys
import xbmcaddon
import xbmc

import time

from libs.api import api_call, set_domain

addon = xbmcaddon.Addon()

time.sleep(60)
interval = 60
next = time.time() + float(interval)

while not xbmc.Monitor().abortRequested():
    if(next < time.time()):
        time.sleep(3)
        if addon.getSetting('username') and len(addon.getSetting('username')) > 0 and addon.getSetting('password') and len(addon.getSetting('password')) > 0: 
            api_call(url = set_domain('https://www.tipsport.cz/rest/client/restrictions/v1/login/duration'), method = 'PUT', novalidate = True)
        next = time.time() + float(interval)
    time.sleep(1)
addon = None