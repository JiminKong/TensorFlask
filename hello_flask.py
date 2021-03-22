from flask import Flask

app = Flask(__name__)

"""
To run this app in PowerShell:
1. $env:FLASK_APP "hello_flask.py"
2. flask run --host=0.0.0.0
"""
@app.route('/')
def hello_flask():
    return "Hello Flask!"
    