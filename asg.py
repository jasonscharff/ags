from flask import Flask
from flask_mongoengine import MongoEngine
import os
import schedule
import time
from flask import  request, Response
from threading import Timer
import datetime
from apscheduler.scheduler import Scheduler

app = Flask(__name__)


if 'MONGODB_URI' in os.environ:
    app.config['MONGODB_SETTINGS'] = {
        'DB' : 'asg',
        'host' : os.environ['MONGODB_URI']
    }
    db = MongoEngine()
else:
    app.config['MONGODB_SETTINGS'] = {'DB': 'asg'}

db = MongoEngine()

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db.init_app(app)

from models import AdminUser

from game_logic import  assign_targets, kill_inactive, mark_dead

def daily_action():
    print 'hello, world'
    kill_inactive()
    assign_targets()
    threading.Timer(60*60*24, daily_action()).start()


import threading

def start_timer():
    x = datetime.datetime.today()
    if x.minute > 29:
        y = x.replace(day=x.day + 1, hour=6, minute=29, second=0, microsecond=0)
        delta_t = y - x
        secs = delta_t.seconds + 1
    else:
        y = x.replace(day=x.day, hour=7, minute=29, second=0, microsecond=0)
        delta_t = y - x
        secs = delta_t.seconds + 1

    threading.Timer(secs, daily_action).start()

start_timer()

from admin_login_manager import *

@app.route('/twilio/dead', methods=['POST'])
def mark_dead_handler():
    body = request.form['Body']
    from_number = request.form['From']
    if AdminUser.objects(phone_number=from_number).count() > 0:
        account_sid = request.form['AccountSid']
        if account_sid == os.environ['TWILIO_SID']:
            status = mark_dead(body)
            if status is True:
                return Response('Success', content_type='text/plain')
            else:
                return Response('Error', content_type='text/plain')
        else:
            return Response('Invalid SID', content_type='text/plain')
    else:
        return Response('Invalid Number', content_type='text/plain')

