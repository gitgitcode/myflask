from flask import Flask
from flask_script import Manager

app = Flask(__name__)

manager = Manager(app)

@manager.command

def hello():
    print "hello!"

if __name__=="__main__":
    manager.run()