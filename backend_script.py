from flask import Flask, request, jsonify, render_template
from datetime import datetime
from functions.urls import normalize_url
from functions.dates import calculate_dates
from functions.data import download_and_store_data
from functions.get_stock_price import stock_price
import pandas as pd

app = Flask(__name__)

@app.route('/' , methods=['GET', 'POST'])
def home():
    # Serve the home page (HTML file)
    return render_template('HTML/Home.html')    

@app.route('/api/stock/chart', methods = ['GET', 'POST'])
def stock_chart():
    data = request.get_json()
    print(data)

    stock_code = data['stock_code']
    time_duration = data['time_duration']

    start_date, end_date = calculate_dates(time_duration = time_duration)

    # print('start_date, end_date',start_date, end_date)
    path = download_and_store_data(stock_symbol = stock_code, start_date = start_date, end_date = end_date)
    
    # print('path', path)
    





@app.route('/api/stock_info', methods=['GET', 'POST'])
def handle_text():
    data = request.get_json()  # Parse JSON data from the request
    print(data)
    if not data or 'stock_code' not in data:
        return jsonify({"message": "Invalid input"}), 400
    
    # Perform some processing (if needed)
    x = data['stock_code'].upper()
    stock_data = stock_price(stock_label = x)
    stock_code = x

    stock_value = stock_data["Stock Price"] # Example stock price

    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    stock_details = stock_data["table_values"]

    # Construct the response
    response = {
        "stock_price": stock_value,
        "formatted_time": formatted_time,
        "stock_details": stock_details
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
