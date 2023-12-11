# -*- coding: utf-8 -*-
import sys
import platform
import xbmcaddon
import xbmcgui

from urllib.parse import urlencode

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
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
