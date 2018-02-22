# !/bin/evn python
from datetime import datetime
from flask import Flask, render_template, url_for
from flask import request
from flask import make_response
from flask import redirect
from flask import abort

from flask_script import Manager
from flask_moment import Moment
from flask_wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import Required


# flask-bootstrap 
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'aaaa11111'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>hello , %s </h1>' % user

def load_user(id):
    return 0

@app.route('/red')
def red():
    return redirect("http://www.google.com")

@app.route('/username/<name>')
def username(name):
    dicts = {'key':123, 'mm':3333}
    comments = dicts
    return render_template('user.html', name=name, mydict=dicts, comments=comments)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    info = ('<span style="color:red">heellloooo!</span>'
            '<p> yours browser is <br/> %s </p>') % user_agent 
    return info

@app.route('/template')
def template():
    return render_template('index.html',  form = NameForm(), current_time = datetime.utcnow())

@app.route('/about')
def about():
    return "<h1>this is about</h1>"

@app.route('/extends')
def extends_page():
    url = url_for('username', name = 'john', _external =True )
    return render_template('extends.html', url = url, current_time = datetime.utcnow())
@app.route('/mm')
def mm():
    return "<h1>this is mm</h1>"

@app.route('/user/<name>') 
def user(name):
    return "<h2> hell, %s !</h2>" % name

@app.route('/admin')
def admin():
    return '<h1>Bad Request</h1>',400

@app.route('/response')
def response():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

@app.route('/form')
def myform():
    return render_template('form.html', form = NameForm() ,current_time = datetime.utcnow())


class NameForm(Form):
    name = StringField('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')



if __name__=="__main__":
    #app.run()
    manager.run()
