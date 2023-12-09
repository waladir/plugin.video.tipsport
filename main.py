# -*- coding: utf-8 -*-1
import os
import sys
import xbmcgui
import xbmcplugin
import xbmcaddon
from xbmcvfs import translatePath

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.driver_utils import get_driver_path

import json
from urllib.parse import parse_qsl,urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

_url = sys.argv[0]
if len(sys.argv) > 1:
    _handle = int(sys.argv[1])
LOGIN_URL = {'CZ' : 'https://www.tipsport.cz/', 'SK' : 'https://www.tipsport.sk/'}
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def check_config():
    addon = xbmcaddon.Addon()
    if not addon.getSetting('username') or not addon.getSetting('password'):
        xbmcgui.Dialog().notification('Tipsport.cz', 'V nastavení je nutné mít vyplněné přihlašovací údaje', xbmcgui.NOTIFICATION_ERROR, 10000)
        sys.exit()


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
        elif addon.getSetting('browser') == 'docker':
            driver = webdriver.Remote(command_executor=addon.getSetting('docker_url'), desired_capabilities=options.to_capabilities())
    except Exception as e:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Problém při volaní prohlížeče. Pokud doplněk předtím fungoval, zkuste restartovat zařízení', xbmcgui.NOTIFICATION_ERROR, 10000)        
        sys.exit()
    if session == True: 
        cookies = load_session()
        if cookies is None:
            login(driver)
            cookies = load_session()
        driver.get('https://www.tipsport.cz/rest/')
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver


def api_call(url):
    data = {}
    try:
        driver = init_driver(session = True)
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
        data = json.loads(driver.find_element(By.TAG_NAME, 'body').text)
    except Exception as e:
        pass
    if 'errorCode' in data:
        try:
            login(driver)
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
            data = json.loads(driver.find_element(By.TAG_NAME, 'body').text)
        except Exception as e:
            pass
    try:
        driver.quit()
    except Exception as e:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Došlo k chybě při volání prohlížeče', xbmcgui.NOTIFICATION_ERROR, 5000)
    return data


def login(driver):
    success = True
    addon = xbmcaddon.Addon()
    LOGIN_BUTTON1 = {'CZ' : 'Přihlásit', 'SK' : 'Prihlásiť'}
    LOGIN_BUTTON2 = {'CZ' : 'Přihlásit se', 'SK' : 'Prihlásiť sa'}
    LOGIN_VERIFICATION = {'CZ' : 'Vložit peníze', 'SK' : 'Vložiť peniaze'}

    addon = xbmcaddon.Addon()
    driver.get(LOGIN_URL[addon.getSetting('tipsport_version')])
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()="' + LOGIN_BUTTON1[addon.getSetting('tipsport_version')] + '"]')))
    login_button = driver.find_element(By.XPATH, '//button[text()="' + LOGIN_BUTTON1[addon.getSetting('tipsport_version')] + '"]')
    login_button.click()

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'username')))
    username = driver.find_element(By.NAME, 'username')
    username.send_keys(addon.getSetting('username'))
    password = driver.find_element(By.NAME, 'password')
    password.send_keys(addon.getSetting('password'))

    login_button = driver.find_element(By.XPATH, '//button[text()="' + LOGIN_BUTTON2[addon.getSetting('tipsport_version')] + '"]')
    login_button.click()
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//a[text()="' + LOGIN_VERIFICATION[addon.getSetting('tipsport_version')] + '"]')))
    except Exception as e:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Došlo k chybě při přihlášení', xbmcgui.NOTIFICATION_ERROR, 5000)
        success = False
    cookies = driver.get_cookies()
    data = json.dumps(cookies)
    save_session(data)
    return success


def save_session(data):
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile'))
    filename = os.path.join(addon_userdata_dir, 'session.txt')
    try:
        with open(filename, "w") as f:
            f.write('%s\n' % data)
    except IOError:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba uložení session', xbmcgui.NOTIFICATION_ERROR, 5000)


def load_session():
    data = None
    addon = xbmcaddon.Addon()
    addon_userdata_dir = translatePath(addon.getAddonInfo('profile'))
    filename = os.path.join(addon_userdata_dir, 'session.txt')
    try:
        with open(filename, "r") as f:
            for row in f:
                session_data = row[:-1]
        data = json.loads(session_data)
    except IOError as error:
        if error.errno != 2:
            xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba načtení session', xbmcgui.NOTIFICATION_ERROR, 5000)
    return data


def play_stream(id, title):
    data = api_call(set_domain('https://www.tipsport.cz/rest/offer/v2/live/matches/' + str(id) + '/stream?deviceType=DESKTOP'))
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
            else:
                url = data['data'].replace('|', '%7C')                
            list_item = xbmcgui.ListItem(path = url)
            list_item.setContentLookup(False)       
            xbmcplugin.setResolvedUrl(_handle, True, list_item)
        else:
            xbmcgui.Dialog().notification('Tipsport.cz', data['data'], xbmcgui.NOTIFICATION_ERROR, 5000)
    else:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při spuštení streamu', xbmcgui.NOTIFICATION_ERROR, 5000)


def list_streams(id, label):
    xbmcplugin.setPluginCategory(_handle, label)
    data = api_call(set_domain('https://www.tipsport.cz/rest/articles/v1/tv/program?day=0&articleId='))
    if 'program' in data:
        for sport in data['program']:
            if sport['id'] == int(id):
                for item in sport['matchesByTimespans']:
                    if len(item) > 0:
                        for i in range(len(item)):
                            if item[i]['live'] == True:
                                print(item[i])
                                list_item = xbmcgui.ListItem(label = item[i]['name'] + '\n' + '[COLOR=gray]' + item[i]['sport'] + ' / ' + item[i]['competition'] + '[/COLOR]')
                                list_item.setInfo('video', {'mediatype':'movie', 'title': item[i]['name']})
                                list_item.setContentLookup(False)
                                list_item.setProperty('IsPlayable', 'true')
                                url = get_url(action = 'play_stream', id = item[i]['id'], title = item[i]['name'])
                                xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
    else:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při načtení streamů', xbmcgui.NOTIFICATION_ERROR, 5000)
    xbmcplugin.endOfDirectory(_handle, cacheToDisc = False)


def list_sports():
    data = api_call(set_domain('https://www.tipsport.cz/rest/articles/v1/tv/program?day=0&articleId='))
    if 'program' in data:
        for sport in data['program']:
            cnt = 0
            for item in sport['matchesByTimespans']:
                for i in range(len(item)):
                    if item[i]['live'] == True:
                        cnt += 1
            if cnt > 0:
                list_item = xbmcgui.ListItem(label = sport['title'])
                url = get_url(action = 'list_streams', id = sport['id'], label = sport['title'])
                xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    else:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Chyba při načtení streamů', xbmcgui.NOTIFICATION_ERROR, 5000)


def list_menu():
    list_sports()
    xbmcplugin.endOfDirectory(_handle, cacheToDisc = False)


check_config()
def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'login':
            driver = init_driver(session = False)
            success = login(driver)
            driver.quit()
            if success == True:
                xbmcgui.Dialog().notification('Tipsport.cz', 'Přihlášení dokončeno', xbmcgui.NOTIFICATION_INFO, 5000)
        elif params['action'] == 'list_streams':
            list_streams(params['id'], params['label'])
        elif params['action'] == 'play_stream':
            play_stream(params['id'], params['title'])
        else:
            raise ValueError('Neznámý parametr: {0}!'.format(paramstring))
    else:
         list_menu()

if __name__ == '__main__':
    router(sys.argv[2][1:])

addon = None
