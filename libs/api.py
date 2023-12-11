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

import json

from libs.session import login, load_session
from libs.utils import user_agent

def set_domain(url):
    addon = xbmcaddon.Addon()
    if addon.getSetting('tipsport_version') == 'SK':
        return url.replace('.cz', '.sk')
    else:
        return url

def init_driver(session = False):
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
    if session == True: 
        cookies = load_session()
        if cookies is None:
            login(driver)
            cookies = load_session()
        driver.get(set_domain('https://www.tipsport.cz/rest/'))
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver

def api_call(url):
    data = {}
    try:
        driver = init_driver(session = True)
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        print(driver.find_element(By.TAG_NAME, 'body').text)        
        data = json.loads(driver.find_element(By.TAG_NAME, 'body').text)
    except Exception as e:
        pass
    if 'errorCode' in data:
        try:
            login(driver)
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
            print(driver.find_element(By.TAG_NAME, 'body').text)        
            data = json.loads(driver.find_element(By.TAG_NAME, 'body').text)
        except Exception as e:
            pass
    try:
        driver.quit()
    except Exception as e:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Došlo k chybě při volání prohlížeče', xbmcgui.NOTIFICATION_ERROR, 5000)
    return data

