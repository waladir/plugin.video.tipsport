# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcaddon
import xbmcgui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.driver_utils import get_driver_path

import requests

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

def get_session():
    cookies = load_session()
    if cookies is None:
        login()
    session = requests.Session()
    for cookie in cookies:
        if cookie['name'] == 'JSESSIONID':
            session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    return session

def make_request(url, method, session):
    headers = {'User-Agent' : user_agent, 'Content-Type' : 'application/json'}
    if method == 'GET':
        data = session.get(url = url, headers = headers)
    elif method == 'PUT':
        data = session.put(url = url, headers = headers)
    return data

def api_call(url, method = 'GET', nolog = False, novalidate = False):
    data = {}
    session = get_session()
    data = make_request(url = url, method = method, session = session).json()
    xbmc.log('Tipsport.cz > ' + str(url))
    if nolog == False or 'errorCode' in data:
        xbmc.log('Tipsport.cz > ' + str(data))
    if 'errorCode' in data and novalidate == False:
        login()
        session.close()
        session = get_session()
        data = make_request(url = url, method = method, session = session).json()
        xbmc.log('Tipsport.cz > ' + str(url))
        if nolog == False or 'errorCode' in data:
            xbmc.log('Tipsport.cz > ' + str(data))
    return data
