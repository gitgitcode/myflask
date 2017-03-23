from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<span style='color:red'>I am app 1</span>"

@app.route('/about')
def about():
    return "<h1>this is about</h1>"

@app.route('/mm')
def mm():
    return "<h1>this is mm</h1>"

if __name__=="__main__":
    app.debug = True
    app.run()
