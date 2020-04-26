from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash
from models import Users
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, LoginManager, login_user, logout_user
from mongoengine.errors import NotUniqueError
import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def check_email(email):  
    if(re.search(regex,email)):  
        return True 
    else:  
        return False 

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = 'secretkey'
login_manager.login_view = 'login'



@app.route('/<path:path>')
def send_assets(path):
    return send_from_directory('static', path)

# LOGIN / LOGOUT >

@login_manager.user_loader
def load_user(user_id):
    return Users.objects(pk=user_id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('login/login.html')
    elif request.method == 'POST':
        p_email = request.form['email']
        p_password = request.form['password']
        if check_email(p_email):
            try:
                user = Users.objects(email = p_email).first()
                if user is None or not check_password_hash(user.password, p_password):
                    flash("Username or password wrong")
                    return redirect(url_for('login'))
                else:
                    login_user(user)
                    return redirect(url_for('index'))
            except:
                flash("Something went wrong")
                return redirect(url_for('login'))
        else:
            flash("Please enter a valid email address")
            return redirect(url_for('login'))
    return True

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('login/register.html')
    elif request.method == 'POST':
        p_name = request.form['name']
        p_password = request.form['password']
        p_email = request.form['email']
        if check_email(p_email):
            try:
                user = Users()
                user.name = p_name
                user.email = p_email
                user.user_type = "Free"
                user.password = generate_password_hash(p_password)
                user.save()
                login_user(user)
            except NotUniqueError as e:
                flash("E-Mail is taken")
                return redirect(url_for("register"))
        else:
            flash("Please enter a valid email address")
            return redirect(url_for('register'))
        return redirect(url_for('index'))
    return True

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# LOGIN / LOGOUT <


@app.route('/')
@login_required
def index():
    return "ok"

# APP RUN >

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True, debug = True)

#APP RUN <
