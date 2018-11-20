from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_login import LoginManager, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/marcio/Projetos/Lucas/app/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'CODEEEEEEEEEEEE'
db = SQLAlchemy(app)
lm = LoginManager(app)
SECRET_KEY="powerful secretkey"
WTF_CSRF_SECRET_KEY="a csrf secret key"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, password):
            self.username = username
            self.password = password

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember-me")


#criando o sistema de login
@property
def is_authenticated(self):
    return True

@property
def is_active(self):
    return True

@property
def is_anonymous(self):
    return False

def get_id(self):
    return str(self.id)

def carregar_usuarios():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
SELECT id, username FROM users;
""")
    return list(cursor)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        n = Users.query.filter_by(username=form.username.data).first()
        print(n)
        print(str(type(n)))
        if n is not None and n.password == form.data['password']:
            login_user(n)   
            flash("Logged in")
    else:
       flash("Invaled Login")
    
    return render_template('login.html', form=form, error=form.errors)

@app.route("/index", methods=['GET','POST'])
@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        i = Users(username=request.form['username'],password=request.form['password'])
        db.session.add(i)
        db.session.commit()
    return render_template('index.html')

@app.route("/cadastrados")
def cadastrados():
    u = carregar_usuarios()
    #print(u)
    return render_template('cadastrados.html', usuarios=u)

@app.route("/delete", methods=['GET','POST'])
def delete():
    if request.method == "POST":
        m = Users.query.filter_by(username=request.form['username']).first()
        db.session.delete(m)
        db.session.commit()       
    u = carregar_usuarios()
    return render_template('cadastrados.html', usuarios=u)

if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()