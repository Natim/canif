# -*- coding: utf-8 -*-
from __future__ import print_function

from flask import Flask, request, render_template, send_file, jsonify
from six import BytesIO

from canif.decorators import jsonp
from canif.exporter import export_insee_data

import logging
logging.basicConfig()

logging.getLogger('elasticsearch').setLevel(logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.DEBUG)

app = Flask(__name__)

# from canif.redis import RedisBackend
# backend = RedisBackend()

from canif.elasticsearch import ElasticsearchBackend
backend = ElasticsearchBackend()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_form():
    communes = [c for c in request.form['cities_val'].split(",") if c]
    variables = [v for v in request.form['variables_val'].split(",") if v]
    filename = "communes-%s-variables-%s.csv" % (
        ','.join(communes), ','.join(variables)
    )
    mimetype = "text/csv"
    output = export_insee_data(backend, communes, variables)
    return send_file(BytesIO(output.read().encode('utf-8')),
                     attachment_filename=filename,
                     as_attachment=True, mimetype=mimetype)


@app.route('/search_variables', methods=['GET'])
@jsonp
def search_variables():
    return jsonify(
        variables=backend.search_variables(request.args.get('query', ""))
    )


@app.route('/search_variables/<var_ids>', methods=['GET'])
@jsonp
def get_variables(var_ids):
    var_ids = var_ids.split(',')
    return jsonify(
        variables=backend.get_variables(var_ids)
    )


@app.route('/search_communes', methods=['GET'])
@jsonp
def search_communes():
    return jsonify(
        communes=backend.search_communes(request.args.get('query', ""))
    )


@app.route('/search_communes/<codgeos>', methods=['GET'])
@jsonp
def get_communes(codgeos):
    codgeos = codgeos.split(',')
    return jsonify(
        communes=backend.get_communes(codgeos)
    )


def serve():
    app.run(debug=True)
