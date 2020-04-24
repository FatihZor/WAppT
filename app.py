from flask import Flask, request, send_from_directory, render_template, redirect, url_for
from models import Users
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, LoginManager, login_user, logout_user

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
app.secret_key = 'secretkey'
login_manager.login_view = 'login'


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
        p_username = request.form['username']
        p_password = request.form['password']
        user = Users.objects(username = p_username).first()
        if user is None or not check_password_hash(user.password, p_password):
            return redirect(url_for('login'))
        else:
            login_user(kullanici)
            return redirect(url_for('index'))
    return True

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('login/register.html')
    elif request.method == 'POST':
        p_name = request.form['name']
        p_username = request.form['username']
        p_password = request.form['password']
        p_email = request.form['email']
        try:
            user = Users()
            user.name = p_name
            user.email = p_email
            user.username = p_username
            user.password = generate_password_hash(p_password)
        except:
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
    app.run(host='0.0.0.0', port=80, threaded=True)

#APP RUN <
