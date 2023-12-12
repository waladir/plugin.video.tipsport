# -*- coding: utf-8 -*-
import os
import xbmcaddon
import xbmcgui
from xbmcvfs import translatePath

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import json

LOGIN_URL = {'CZ' : 'https://www.tipsport.cz/', 'SK' : 'https://www.tipsport.sk/'}

def login():
    from libs.api import init_driver
    driver = init_driver()
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
    try:
        driver.quit()
    except Exception as e:
        xbmcgui.Dialog().notification('Tipsport.cz', 'Došlo k chybě při volání prohlížeče', xbmcgui.NOTIFICATION_ERROR, 5000)
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

