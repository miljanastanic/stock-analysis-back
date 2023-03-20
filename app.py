import json
from pickle import GET

from flask import Flask, request
from flask_cors import CORS

import dataframe
import predicting
from tabulate import tabulate
from flask import jsonify
from flask import send_file
import os


app = Flask(__name__)
CORS(app)


@app.route('/data', methods=['GET'])
def my_data():  # put application's code here
    dict = dataframe.get_data_frame()
    JSONP_data = jsonify(dict)
    return JSONP_data


@app.route('/cv', methods=['GET'])
def my_plots_cv():
    file = dataframe.descriptive_historical_cv()
    return send_file(file)


@app.route('/vos', methods=['GET'])
def my_plots_vos():
    file = dataframe.descriptive_historical_vos()
    return send_file(file)


@app.route('/moving', methods=['GET'])
def my_map():
    #http://127.0.0.1:5000/moving?day1=20&day2=30&day3=40
    day1 = request.args.get('day1', None)
    day2 = request.args.get('day2', None)
    day3 = request.args.get('day3', None)
    print(day1, day2, day3)
    file = dataframe.moving_average_price(day1, day2, day3)
    return send_file(file)


@app.route('/dr', methods=['GET'])
def my_plots_dr():
    file = dataframe.daily_returns()
    return send_file(file)


@app.route('/adr', methods=['GET'])
def my_plots_adr():
    file = dataframe.avg_daily_returns()
    return send_file(file)


@app.route('/correlation', methods=['GET'])
def correlation():
    file = dataframe.correlation()
    return send_file(file)


@app.route('/risk', methods=['GET'])
def risk():
    file = dataframe.risk()
    return send_file(file)


@app.route('/model', methods=['GET'])
def model():
    # http://127.0.0.1:5000/model?code='AMZN'
    code = request.args.get('code', None)
    print(code)
    file = predicting.predict(str(code))
    return send_file(file)


@app.route('/docs', methods=['GET'])
def get_docs():
    file_path = os.path.join(os.path.dirname(__file__), 'docs.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/docs/<int:id>', methods=['GET'])
def get_doc(id):
    file_path = os.path.join(os.path.dirname(__file__), 'docs.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    for obj in data['blogs']:
        if obj['id'] == int(id):
            return jsonify(obj)
    return jsonify({'error' : 'Object not found'})


with app.test_request_context():
    df = dataframe.get_data_frame()

    print(tabulate(df, headers='keys'))

if __name__ == '__main__':
    app.run(debug=True)

