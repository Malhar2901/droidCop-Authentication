import urllib.parse
from markupsafe import Markup
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt

app = Flask(__name__)
password = urllib.parse.quote_plus("ManasiMalhar@9701")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{password}@localhost/dCOP'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt(app)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class LoginForm(FlaskForm):

    email = EmailField(validators=[
        InputRequired() ], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
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
            new_user = User(username=data["username"], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
        else:
            return {"status": "Failure", "message": "Invalid inputs"}, 403, {"Content-Type": "application/json"}
    else:
        return {"status": "Failure", "message": "No username or password"}, 403, {"Content-Type": "application/json"}

    return {"status": "Success", "message": "User Registered"}, 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run(debug=True)
