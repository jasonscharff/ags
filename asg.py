from flask import Flask
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)


# if 'MONGODB_URI' in os.environ:
#     app.config['MONGODB_SETTINGS'] = {
#         'DB' : 'test', #remember to change this to prod.
#         'host' : os.environ['MONGODB_URI']
#     }
#     db = MongoEngine()
# else:
app.config['MONGODB_SETTINGS'] = {'DB': 'asg'}
db = MongoEngine()

app.config['SECRET_KEY'] = '123'

db.init_app(app)

from models import AdminUser

from admin_login_manager import *
from game_logic import  assign_targets, mark_dead, kill_inactive
from mailer import send_new_target, send_post_kill
#assign_targets()
#mark_dead('5')
# kill_inactive()

