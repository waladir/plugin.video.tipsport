# -*- coding: utf-8 -*-
import os
import sys
import xbmcgui
import xbmcplugin
import xbmcaddon

import json
from urllib.parse import parse_qsl
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from libs.lists import list_sports, list_streams, list_settings, list_blacklist
from libs.blacklist import add_to_blacklist, remove_from_blacklist
from libs.api import api_call, set_domain
from libs.session import login, export_jsessionid
from libs.utils import user_agent, check_config, get_url

if len(sys.argv) > 1:
    _handle = int(sys.argv[1])

def play_stream(id, title):
    data = api_call(url = set_domain('https://www.tipsport.cz/rest/offer/v2/live/matches/' + str(id) + '/stream?deviceType=DESKTOP'))
    if 'data' in data:
        if 'http' in data['data']:
            if data['type'] == 'URL_IMG':
                headers = {'User-Agent' : user_agent, 'Accept' : '*/*', 'Content-type' : 'application/json;charset=UTF-8'}
                request = Request(url = data['data'], headers = headers)
                try:
                    response = urlopen(request)
                    html = response.read()
                    if html and len(html) > 0:
                        data = json.loads(html)
                        if 'hlsUrl' not in data:
                            xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při spuštení streamu', xbmcgui.NOTIFICATION_ERROR, 5000)
                            return
                        else:
                            url = data['hlsUrl']
                except HTTPError as e:
                    xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při spuštení streamu', xbmcgui.NOTIFICATION_ERROR, 5000)
                    return
            elif data['type'] == 'URL_TVCOM':
                headers = {'User-Agent' : user_agent, 'Accept' : '*/*', 'Content-type' : 'application/json;charset=UTF-8'}
                request = Request(url = data['data'], headers = headers)
                try:
                    response = urlopen(request)
                    html = response.read()
                    if html and len(html) > 0:
                        data = json.loads(html)
                        if 'url' not in data or 'hls' not in data['url']:
                            xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při spuštení streamu', xbmcgui.NOTIFICATION_ERROR, 5000)
                            return
                        else:
                            url = data['url']['hls']['url']
                except HTTPError as e:
                    xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při spuštení streamu', xbmcgui.NOTIFICATION_ERROR, 5000)
                    return
            elif 'URL' in data['type']:
                xbmcgui.Dialog().notification('Tipsport.cz', 'Nepodporovaný typ stremu: ' + data['type'], xbmcgui.NOTIFICATION_ERROR, 5000)
                return
            else:
                url = data['data'].replace('|', '%7C')   
            list_item = xbmcgui.ListItem(path = url)
            list_item.setContentLookup(False)       
            xbmcplugin.setResolvedUrl(_handle, True, list_item)
        else:
            xbmcgui.Dialog().notification('Tipsport.cz', data['data'], xbmcgui.NOTIFICATION_ERROR, 5000)
    else:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při spuštení streamu', xbmcgui.NOTIFICATION_ERROR, 5000)

def list_menu():
    addon = xbmcaddon.Addon()
    icons_dir = os.path.join(addon.getAddonInfo('path'), 'resources','images')    
    list_sports()
    list_item = xbmcgui.ListItem(label='Nastavení')
    url = get_url(action='list_settings', label = 'Nastavení')  
    list_item.setArt({ 'thumb' : os.path.join(icons_dir , 'settings.png'), 'icon' : os.path.join(icons_dir , 'settings.png') })
    xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.endOfDirectory(_handle, cacheToDisc = False)

check_config()

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'login':
            success = login()
            if success == True:
                xbmcgui.Dialog().notification('Tipsport.cz', 'Přihlášení dokončeno', xbmcgui.NOTIFICATION_INFO, 5000)
        elif params['action'] == 'list_streams':
            list_streams(params['id'], params['label'])
        elif params['action'] == 'play_stream':
            play_stream(params['id'], params['title'])

        elif params['action'] == 'list_settings':
            list_settings(params['label'])
        elif params['action'] == 'addon_settings':
            xbmcaddon.Addon().openSettings()            

        elif params['action'] == 'list_blacklist':
            list_blacklist(params['label'])
        elif params['action'] == 'add_to_blacklist':
            add_to_blacklist(params['type'], params['name'])
        elif params['action'] == 'remove_from_blacklist':
            remove_from_blacklist(params['type'], params['name'])
        elif params['action'] == 'export_jsessionid':
            export_jsessionid()


        else:
            raise ValueError('Neznámý parametr: {0}!'.format(paramstring))
    else:
         list_menu()

if __name__ == '__main__':
    router(sys.argv[2][1:])

addon = None
