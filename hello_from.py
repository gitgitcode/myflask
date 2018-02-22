from flask import Flask, render_template, url_for
from flask_wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from flask_script import Manager
from flask_moment import Moment


class NameForm(Form):
    name = StringFiled('what is your name?', validators=[Required()])
    submit = SubmitField('Submit')

