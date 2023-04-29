import sqlite3
import urllib.parse
from markupsafe import Markup
from flask import Flask, render_template, url_for, redirect, request
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt

DB_PATH="db/login"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
bcrypt = Bcrypt(app)

login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()
    curs.execute("SELECT * FROM login WHERE id = (?)", [user_id])
    data = curs.fetchone()
    conn.close()
    if data is None:
        return None
    return User(int(data[0]), data[1], data[2])


class User(UserMixin):
    def __init__(self,id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.authenticated = False
    
    def is_authenticated(self):
        return self.authenticated

class LoginForm(FlaskForm):

    email = EmailField(validators=[
        InputRequired() ], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect(DB_PATH)
        curs = conn.cursor()
        curs.execute("SELECT * FROM login where username = (?)", [form.email.data])
        data = list(curs.fetchone())
        user = load_user(data[0])
        conn.close()
        print(user.username)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('dchomepage.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dcoperation.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if "username" in data and "password" in data:
        if len(data["username"]) >= 2 and len(data["password"]) >= 6:
            hashed_password = bcrypt.generate_password_hash(data["password"])
            conn = sqlite3.connect(DB_PATH)
            curs = conn.cursor()
            curs.execute("INSERT INTO login(username, password) VALUES(?,?)", [data["username"], hashed_password])
            conn.commit()
            conn.close()
            # new_user = User(username=data["username"], password=hashed_password)
            # db.session.add(new_user)
            # db.session.commit()
        else:
            return {"status": "Failure", "message": "Invalid inputs"}, 403, {"Content-Type": "application/json"}
    else:
        return {"status": "Failure", "message": "No username or password"}, 403, {"Content-Type": "application/json"}

    return {"status": "Success", "message": "User Registered"}, 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run(debug=True)
