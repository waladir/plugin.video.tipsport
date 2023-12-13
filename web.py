# -*- coding: utf-8 -*-
import os
import xbmcaddon

from bottle import run, route, post, template, request, static_file
import json

from libs.session import save_session

addon = xbmcaddon.Addon()
template_dir = os.path.join(addon.getAddonInfo('path'), 'resources','templates')
image_dir = os.path.join(addon.getAddonInfo('path'), 'resources','images')
addon = None

@route('/img/<image>')
def add_image(image):
    return static_file(image, root = image_dir)


@route('/')
@post('/')
def page():
    message = ''
    if request.params.get('jsessionid') is not None:
        jsessionid = request.params.get('jsessionid').strip()
        if len(jsessionid) == 0:
            message = 'Nezadaná žádná hodnota JSESSIONID!'
        elif '.czp-wt' not in jsessionid:
            message = 'Chybná hodnota JSESSIONID! Přesvědčte se, že jste vložily celou hodnotu!'
        else:
            cookie = [{'domain' : '.tipsport.cz', 'name' : 'JSESSIONID', 'value' : str(jsessionid)}]
            save_session(json.dumps(cookie))
            message = 'Hodnota JSESSIONID uložena do doplňku.'

    return template(os.path.join(template_dir, 'form.tpl'), message = message)

def start_server():
    run(host = '0.0.0.0', port = 8089)

