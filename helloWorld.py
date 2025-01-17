# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:19:53 2024

@author: DanielDomikaitis
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
