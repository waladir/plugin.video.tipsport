# -*- coding: utf-8 -*-
import xbmcaddon
import xbmc

import time
import threading

from libs.api import api_call, set_domain
from libs.session import export_jsessionid
import web

addon = xbmcaddon.Addon()

class BottleThreadClass(threading.Thread):
    def run(self):
        web.start_server()

time.sleep(10)
bt = BottleThreadClass()
bt.start()

time.sleep(50)
interval = 60
next = time.time() + float(interval)
# next_export = time.time()

while not xbmc.Monitor().abortRequested():
    if(next < time.time()):
        time.sleep(3)
        if addon.getSetting('username') and len(addon.getSetting('username')) > 0 and addon.getSetting('password') and len(addon.getSetting('password')) > 0: 
            api_call(url = set_domain('https://www.tipsport.cz/rest/client/restrictions/v1/login/duration'), method = 'PUT', novalidate = True)
        next = time.time() + float(interval)
    # if(next_export < time.time()):
    #     time.sleep(3)
    #     if addon.getSetting('username') and len(addon.getSetting('username')) > 0 and addon.getSetting('password') and len(addon.getSetting('password')) > 0 and addon.getSetting('jsession_file_folder') and len(addon.getSetting('jsession_file_folder')) > 0: 
    #         export_jsessionid(silent = True)
    #     next_export = time.time() + float(60*60*3)
    time.sleep(1)
addon = None
