from flask import Flask
from flask_mongoengine import MongoEngine
import os
import schedule
import time
from flask import  request

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
from game_logic import  assign_targets, kill_inactive

def daily_action():
    kill_inactive()
    assign_targets()

schedule.every().day.at("12:00").do(daily_action)

@app.route('/twilio/dead', methods=['POST'])
def mark_dead():
    body = request.form['Body']
    from_number = request.form['From']
    if AdminUser.objects(phone_number=from_number).count() > 0:
        account_sid = request.form['AccountSid']
        if account_sid == os.environ['TWILIO_SID']:
            status = mark_dead(body)
            if status is True:
                return 'Success'
            else:
                return 'Error'
        else:
            return 'Invalid SID'
    else:
        'return invalid number'

