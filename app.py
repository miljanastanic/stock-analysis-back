from pickle import GET

from flask import Flask, request

import dataframe
import predicting
from tabulate import tabulate
from flask import jsonify
from flask import send_file


app = Flask(__name__)


@app.route('/data', methods=['GET'])
def my_data():  # put application's code here
    df = dataframe.get_data_frame()
    dict = []
    for index, row in df.iterrows():
        # print('index: ', index)
        # print('row: ', row)
        dict1 = {}
        dict1['date'] = str(index)
        for c, v in row.items():
            # print('columnName', c)
            # print('value', v)
            s = str(c).lower()
            dict1[s] = v

        dict.append(dict1)
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
    file = predicting.predict(code)
    return send_file(file)


with app.test_request_context():
    df = dataframe.get_data_frame()

    #print(tabulate(df, headers='keys'))

if __name__ == '__main__':
    app.run()

