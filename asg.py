from flask import Flask
from flask_mongoengine import MongoEngine
import os
import schedule
import time
from flask import  request, Response
from threading import Thread

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

from admin_login_manager import *
from game_logic import  assign_targets, kill_inactive, mark_dead

def daily_action():
    kill_inactive()
    assign_targets()

def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every().day.at("12:00").do(daily_action)
schedule.run_pending()

t1 = Thread(target = schedule_loop)
t1.setDaemon(True)
t1.start()


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

