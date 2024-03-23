import re
from flask import Flask, render_template, request

 
# Create a flask application
app = Flask(__name__)


@app.get('/')
def index():
    return render_template('index.html')

@app.get('/upload')
def upload():
    return render_template('upload.html')

@app.get('/maps')
def maps():
    return render_template('map.html')
