from flask_script import Manager

from myapp import app

manager = Manager(app)

@manager.commd

def hello():
    print "Hello"

if __name__=="__main__":
    manager.run()