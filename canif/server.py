# -*- coding: utf-8 -*-
from __future__ import print_function

from flask import Flask, request, render_template, send_file
from werkzeug import secure_filename


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def serve():
    app.run(debug=True)
