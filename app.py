from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from urllib.parse import quote
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisissupposedtobesecret!"

# ] = "sqlite:///C:\\Users\\damodar.pulimamidi\\Desktop\\16march\\singleapp\\database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://jpr@avistosdb01:%s@avistosdb01.mysql.database.azure.com/avistos" % quote('Prakash.881')




db = SQLAlchemy(app)
migrate = Migrate(app, db)


# class User( db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(80))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(100))
    client = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    role = StringField("role", validators=[InputRequired(), Length(min=4, max=25)])
    client = StringField("client ", validators=[InputRequired(), Length(min=4, max=25)])
    remember = BooleanField("remember me")


class RegisterForm(FlaskForm):
    email = StringField(
        "email",
        validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)],
    )
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    role = StringField("role", validators=[InputRequired(), Length(min=4, max=25)])
    client = StringField("client ", validators=[InputRequired(), Length(min=4, max=25)])
    remember = BooleanField("remember me")


@app.route("/")
def index1():
    return render_template("index1.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

            # if check_password_hash(user.password, form.password.data):
            #     login_user(user, remember=form.remember.data)
            #     return redirect(url_for("dashboard"))

        return "<h1>Invalid username or password</h1>"
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template("login.html", form=form)
    # return render_template("dashboard.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        # hashed_password = generate_password_hash(form.password.data, method="sha256")
        password1 = (form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            client=form.client.data,
            password=password1,
        )
        db.session.add(new_user)
        db.session.commit()

        return "<h1>New user has been created!</h1>"
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template("signup.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username)
    # return render_template('tagger.html',name=current_user.username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index1"))


admin = Admin(app)
admin.add_view(ModelView(User, db.session))


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug="True", host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))