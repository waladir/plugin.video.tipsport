# -*- coding: utf-8 -*-
import os
import xbmcaddon
import xbmcgui
from xbmcvfs import translatePath

import json

def add_to_blacklist(type, name):
    blacklist = load_blacklist()
    competitions = blacklist['competitions']
    sports = blacklist['sports']
    if type == 'competitions' and name not in competitions:
        competitions.append(name)
    if type == 'sports' and name not in sports:
        sports.append(name)
    xbmcgui.Dialog().notification('Tipsport.cz', name + ' přidáno na blacklist', xbmcgui.NOTIFICATION_INFO, 5000)    
    blacklist = {'competitions' : competitions, 'sports' : sports}
    save_blacklist(blacklist)

def remove_from_blacklist(type, name):
    blacklist = load_blacklist()
    competitions = blacklist['competitions']
    sports = blacklist['sports']
    if type == 'competitions' and name in competitions:
        competitions.remove(name)
    if type == 'sports' and name in sports:
        sports.remove(name)
    xbmcgui.Dialog().notification('Tipsport.cz', name + ' odstraněno z blacklistu', xbmcgui.NOTIFICATION_INFO, 5000)    
    blacklist = {'competitions' : competitions, 'sports' : sports}
    save_blacklist(blacklist)

def load_blacklist():
    competitions = []
    sports = []
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile')) 
    filename = os.path.join(addon_userdata_dir, 'blacklist.txt')
    try:
        with open(filename, 'r') as file:
            with open(filename, "r") as f:
                for row in f:
                    data = json.loads(row[:-1])
        if 'sports' in data:
            sports = data['sports']
        if 'competitions' in data:
            competitions = data['competitions']
    except IOError as error:
        if error.errno != 2:
            xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při načtení blacklistu', xbmcgui.NOTIFICATION_ERROR, 5000)
    return {'competitions' : competitions, 'sports' : sports}

def save_blacklist(blacklist):
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile')) 
    filename = os.path.join(addon_userdata_dir, 'blacklist.txt')
    try:
        with open(filename, "w") as f:
            f.write('%s\n' % json.dumps(blacklist))
    except IOError:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba uložení blacklistu', xbmcgui.NOTIFICATION_ERROR, 5000)            
