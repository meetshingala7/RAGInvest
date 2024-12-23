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
    # Refers to the search page
    return render_template('HTML/Home.html')    

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    # Refers to the registration page
    return render_template('HTML/registration.html')


@app.route('/api/stock/chart', methods = ['GET', 'POST'])
def stock_chart():
    # Collect data from request
    data = request.get_json()
    print(data)

    if not data:
        # Vaildate the request payload is not empty
        return jsonify({'error':'Invalid input. JSON data is required.'}), 400


    if 'stock_code' not in data.keys():        
        # Ensures that stock code is not Null
        return jsonify({'error': 'Stock code is required'}), 400

    # Get Stock Code from request payload by user
    stock_code = data['stock_code']

    if 'time_duration' not in data.keys():
        # If the time duration comes as null. Default time is queried
        path = download_and_store_data(stock_symbol = stock_code)
    else:
        try:
            # Get Time duration from request payload by user    
            time_duration = data['time_duration']

            # Both the stock code and time duration is received successfully
            # Based on Time Duration, Start and End date is calculated
            end_date, start_date = calculate_dates(time_duration = time_duration)

            # print('start_date, end_date',start_date, end_date)
            # From the above calculated date, the historical data is brought using the function
            # The path of the file is returned for further processing 
            path = download_and_store_data(stock_symbol = stock_code, start_date = start_date, end_date = end_date)
        except Exception as e:
            # If anything function fails, the error response is returned
            return jsonify({'error': f'Calculating Dates {str(e)}'}), 500
        
    print(path)
    # print('path', path)
    
    import pandas as pd
    import numpy as np
    import json
    try:
        # Read the Parquet file
        df = pd.read_parquet(path)
        # If the column is an instance of pd.DatetimeIndex, 
        # Ensure that the index is converted to strings and hence list
        # Else Convert straight to list
        if isinstance(df.index, pd.DatetimeIndex):
            x = df['Close'].index.strftime('%Y-%m-%d').tolist()  
        else:
            x = df.index.tolist()
        # Convert the stock code for the data in dataframe
        stock_symbol = f'{stock_code}.NS'
        y = df['Close'][f'{stock_symbol}'].values.tolist()
        # print('x', x)
        # print('y', y)
    except KeyError as e:
        print(e)

        response = {
            'response' : 'There is no data for stock symbol'
        }

        return jsonify(response), 404
    else:
        response = {
            'x_axis' : x,
            'y_axis' : y
        }
        return jsonify(response), 200



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

@app.route('/api/validate-user', methods = ['POST'])
def validate_user():
    data = request.get_json()

    if not data:
        return jsonify({'isValid': False,'error': 'The username and Email id is required'}), 400

    if 'username' not in data.keys():
        return jsonify( {
            'isValid' : False , 
            "errors": {
                "username" : 400,
                "email" : 400
            }
        }), 200
        return jsonify({'isValid': False,'error': 'The username is not present'}), 400
    
    username = data['username']

    if 'email' not in data.keys():
        return jsonify( {
            'isValid' : False , 
            "errors": {
                "username" : 500,
                "email" : 500
            }
        }), 500
    
    email = data['email']

    import psycopg2
    try:
        conn = psycopg2.connect(
            dbname = "postgres",
            user = "postgres",
            password = "secretpswd",
            host = "localhost",
            port = 5432
        )

        cur = conn.cursor()

        query_username = """
        SELECT
            username,
            email_id
        FROM
            postgres.public.users
        WHERE
            username = %s;
        """

        cur.execute(query_username, (str(username), ))

        row_username = cur.fetchall()
        print(row_username)
        
        query_email = """
        SELECT
            username,
            email_id
        FROM
            postgres.public.users
        WHERE
            email_id = %s;
        """

        cur.execute(query_email, (str(email), ))

        row_email= cur.fetchall()
        print(row_email)

        # If username is in use
        # CONDITION 1
        if not row_email and row_username:
            return jsonify( {
                'isValid' : False , 
                "errors": {
                    "username" : 'The username is in use',
                    "email" : ''
                }
            }), 400
            # return '1'
        
        # If email is in use
        # CONDITION 2
        elif not row_username and row_email:
            return jsonify( {
                'isValid' : False , 
                "errors": {
                    "username" : '',
                    "email" : 'The email is in use'
                }
            }), 400
            # return '2'

        # Both email and username is in use
        # CONDITION 3
        elif not row_username and not row_email:
            return jsonify( {
                'isValid' : True , 
                "errors": {
                    "username" : '',
                    "email" : ''
                }
            }), 200
            return '3'


        # Both are open
        # CONDITION 4
        else:
            return jsonify( {
                'isValid' : False , 
                "errors": {
                    "username" : 'The username is in use',
                    "email" : 'The Email ID is in use'
                }
            }), 400
            # return '4'
                
    except Exception as e:
        print(str(e))




if __name__ == '__main__':
    app.run(debug=True)
