from wtforms import form, fields, validators
from models import AdminUser, Assassin
from flask_admin.contrib.mongoengine import ModelView
import flask_login as login
from asg import app
from flask import Flask, url_for, redirect, render_template, request
from flask_admin import helpers, expose
import flask_admin as admin


class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = AdminUser.objects(username=self.login.data).first()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not AdminUser.validate_login(user.hashed_password, self.password.data.encode('UTF_8')):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return AdminUser.objects(username=self.login.data).first()


def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(username):
        return AdminUser.objects(username=username).first()

    admin_view = admin.Admin(app, 'AGS', index_view=SecureAdminIndexView(), base_template='my_master.html')

    admin_view.add_views(SecureModelView(AdminUser))
    admin_view.add_views(SecureModelView(Assassin))

    app.run(port=5000)



class SecureAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(SecureAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = 'If you need admin access, see Jason Scharff'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(SecureAdminIndexView, self).index()

class SecureModelView(ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

init_login()