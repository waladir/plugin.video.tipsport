# -*- coding: utf-8 -*-
import sys
import xbmcaddon
import xbmcgui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.driver_utils import get_driver_path

from urllib.parse import unquote
import requests
import json

from libs.session import login, load_session
from libs.utils import user_agent

def set_domain(url):
    addon = xbmcaddon.Addon()
    if addon.getSetting('tipsport_version') == 'SK':
        return url.replace('.cz', '.sk')
    else:
        return url

def init_driver():
    addon = xbmcaddon.Addon()
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1200,800')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--remote-debugging-port=9222')
    # options.add_argument('--blink-settings=imagesEnabled=false')
    # options.add_argument('--host-resolver-rules=MAP *.pilling.com 127.0.0.1, MAP *.casinomodule.com, MAP *.twitter.com 127.0.0.1, MAP *.ads-twitter.com 127.0.0.1, MAP *.smartlook.com 127.0.0.1, MAP *.doubleclick.net 127.0.0.1, MAP *.adform.net 127.0.0.1, MAP *.t.co 127.0.0.1, MAP *.googletagmanager.com 127.0.0.1')
    options.add_argument('--no-proxy-server')
    options.add_argument('--user-agent=' + user_agent)
    caps = DesiredCapabilities().CHROME
    options.page_load_strategy = 'none'
    caps['pageLoadStrategy'] = 'none'
    try:
        if addon.getSetting('browser') == 'lokální Google Chrome':
            driverPath = str(get_driver_path('chromedriver'))
            driver = webdriver.Chrome(driverPath, options=options, desired_capabilities=caps)
        elif addon.getSetting('browser') == 'Selenium Grid':
            driver = webdriver.Remote(command_executor=addon.getSetting('docker_url'), desired_capabilities=options.to_capabilities())

    except Exception as e:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Problém při volaní prohlížeče. Pokud doplněk předtím fungoval, zkuste restartovat zařízení', xbmcgui.NOTIFICATION_ERROR, 10000)        
        sys.exit()
    return driver

def api_call(url):
    requests_cookies = {}
    cookies = load_session()
    s = requests.Session()    
    for cookie in cookies:
        if 'httpOnly' in cookie:
            httpO = cookie.pop('httpOnly')
            cookie['rest'] = {'httpOnly': httpO}
        if 'expiry' in cookie:
            cookie['expires'] = cookie.pop('expiry')
        cookie.pop('sameSite')
        s.cookies.set(**cookie)
        requests_cookies[cookie['name']] = unquote(cookie['value'])

    headers = {'User-Agent' : user_agent, 'Accept' : '*/*', 'Content-type' : 'application/json;charset=UTF-8', 'DNT' : '1', 'Host' : 'www.tipsport.cz', 'Referer' : 'https://www.tipsport.cz/tv', 'Sec-Fetch-Dest' : 'empty', 'Sec-Fetch-Mode' : 'cors', 'Sec-Fetch-Site' : 'same-origin'} 
    r = s.get(url = url, headers = headers)
    print(r.text)
    data = json.loads(r.text)
    return data

def get_session():
    cookies = load_session()
    if cookies is None:
        login()
    session = requests.Session()
    for cookie in cookies:
        if cookie['name'] != '':
            session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    return session

def api_call(url):
    headers = {'User-Agent' : user_agent, 'Content-Type' : 'application/json'}
    data = {}
    session = get_session()
    data = session.get(url = url, headers = headers).json()
    print(data)
    if 'errorCode' in data:
        login()
        session.close()
        session = get_session()
        data = session.get(url = url, headers = headers).json()
        print(data)
    return data
