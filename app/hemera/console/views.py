#-*- coding: UTF-8 -*-

import time
import os
import subprocess
import yaml
from flask import Blueprint, render_template, session
from flask import jsonify, abort, make_response, request
from .. import app

cns = Blueprint('cns', __name__, template_folder='templates', static_folder='static')

@cns.route('/lau_out')
def lau_out():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        if not ws.closed:
            popen = subprocess.Popen(['tailf', '/search/odin/flasky/app/hemera/console/lau.out'], stdout = subprocess.PIPE)
            while True:
                message = popen.stdout.readline()
                ws.send(message)
            else:
                abort(404)
        return "Connected."
    else:
        return "Unconnected."
