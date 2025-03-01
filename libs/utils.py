# -*- coding: utf-8 -*-
import sys
import os
import platform
import xbmcaddon
import xbmcgui
import xbmc

import json 
from io import BytesIO
from zipfile import ZipFile
import shutil

from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0'
plugin_id = 'plugin.video.tipsport'

_url = sys.argv[0]

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def check_config():
    addon = xbmcaddon.Addon()
    if not addon.getSetting('username') or not addon.getSetting('password'):
        xbmcgui.Dialog().notification('Tipsport.cz', 'V nastavení je nutné mít vyplněné přihlašovací údaje', xbmcgui.NOTIFICATION_ERROR, 10000)
        sys.exit()
    if addon.getSetting('browser') == 'lokální Google Chrome' and not('amd' in platform.machine().lower() or '86' in platform.machine().lower()):
        xbmcgui.Dialog().textviewer('Tipsport.cz', 'Pro fungování doplňku na vaší platformě je vyžadovaný Selenium Grid. Použití lokálního Google Chrome prohlížeče bohužel není možné. Návod na zprovoznění ve formě docker kontajneru v CoreELEC/LibreELEC nebo informace o případném řešení pro jiné platformy najdete v prvním příspěvku ve vlákně k doplňku na XBMC Kodi CZ/SK fóru:\n\nhttps://www.xbmc-kodi.cz/prispevek-tipsport-cz\n\nV nastavení doplku je pak nutné jako prohlížeč vybrat Selenium Grid.')
        sys.exit()
    if addon.getSetting('browser') == 'načíst ze souboru' and len(addon.getSetting('jsession_file_folder')) == 0:
        xbmcgui.Dialog().textviewer('Tipsport.cz', 'Pro načtení JSESSIONID ze souboru je nutné zadat adresář, kde je umístěný!')
        sys.exit()

def check_chromedriver(path):
    data = None
    split_path = path.split(os.sep)
    if len(split_path) > 2:
        platform = split_path[-2]
        driverpath = os.path.split(path)[0]
        filename = os.path.join(driverpath, 'version.json')
        version = None
        try:
            with open(filename, "r") as f:
                for row in f:
                    version = row[:-1]
        except IOError:
            pass
        request = Request(url = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json', method = 'GET', headers = {'User-Agent' : user_agent, 'Accept': 'application/json', 'Content-Type' : 'application/json'})
        try:
            response = urlopen(request).read()
            data = json.loads(response)
        except HTTPError as e:
            xbmc.log('Tipsport.cz > ' 'Chyba při kontrole verze chromedriver: ' + e.reason)
            return { 'err' : e.reason }  
        if data is not None and 'channels' in data and 'Stable' in data['channels'] and 'downloads' in data['channels']['Stable']:
            if version is None or version != data['channels']['Stable']['version']:
                xbmcgui.Dialog().notification('Tipsport.cz', 'Nalezena nová verze chromedriveru!', xbmcgui.NOTIFICATION_INFO, 5000)
                for platforms in data['channels']['Stable']['downloads']['chromedriver']:
                    if platform == platforms['platform']:
                        response = urlopen(platforms['url'])
                        zip = ZipFile(BytesIO(response.read()))
                        for file in zip.namelist():
                            zipfile = os.path.basename(file)
                            if zipfile:
                                source = zip.open(file)
                                target = open(os.path.join(driverpath, zipfile), "wb")
                                with source, target:
                                    shutil.copyfileobj(source, target)
                        xbmcgui.Dialog().notification('Tipsport.cz', 'Chromedriver byl aktualizovaný!', xbmcgui.NOTIFICATION_INFO, 5000)
                        try:
                            with open(filename, "w") as f:
                                f.write('%s\n' % data['channels']['Stable']['version'])
                        except IOError:
                            pass



    