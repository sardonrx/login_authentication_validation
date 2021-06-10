from enum import unique
from re import M
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisissusansecretkey'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), unique= True, nullable=False)
    password = db.Column(db.String(80), nullable= False)

class RegisterForm(FlaskForm):
    username = StringField(validators= [InputRequired(), Length(min=4, max= 20)], render_kw={"placeholder":"username"})
    password = PasswordField(validators= [InputRequired(), Length(min=4, max= 20)], render_kw={"placeholder":"password"})
    submit = SubmitField()

    def validating_user(self, username):
        existing_username= User.query.filter_by(
            username=username.data).first()
        
        if existing_username:
            raise ValidationError('This username already exist')
class LoginForm(FlaskForm):
    username = StringField(validators = [InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"username"})
    password = PasswordField(validators = [InputRequired(), Length(min=4, max= 20)], render_kw={"placeholder":"password"})
    submit = SubmitField()

@app.route('/' )
def home():
    return render_template('home.html')

@app.route('/login', methods= ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register', methods= ['GET', 'POST'])
def register():
    form= RegisterForm()

    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit
        
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)