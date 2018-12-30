'''
Kei Imada
20181229

Flask server for prereqvis
'''

import os
import json

from flask import Flask, request, render_template, jsonify, send_from_directory

GRAPH_PATH = 'static/data/graph.json'
app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/graph', methods=['GET'])
def get_next_frame():
    ''' gets graph data '''
    with app.open_resource(GRAPH_PATH) as gf:
        graph = json.load(gf)
    return jsonify(graph)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
