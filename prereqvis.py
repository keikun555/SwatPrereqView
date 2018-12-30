'''
Kei Imada
20181229

Flask server for prereqvis
'''

import os
import json

from flask import Flask, request, render_template, jsonify, abort

GRAPH_PATH = 'static/data/graph.json'
app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/graph', methods=['GET'])
def get_next_frame():
    ''' gets graph data '''
    return jsonify(json.load(open(GRAPH_PATH, 'r')))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
