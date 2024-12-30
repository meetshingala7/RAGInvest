from flask import Flask, request, jsonify, render_template
from datetime import datetime
from functions.urls import normalize_url
from functions.dates import calculate_dates
from functions.data import download_and_store_data
from functions.get_stock_price import stock_price
import pandas as pd
import json

app = Flask(__name__)

@app.route('/' , methods=['GET', 'POST'])
def home():
    # Refers to the search page
    return render_template('HTML/Home.html')    

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    # Refers to the registration page
    return render_template('HTML/registration.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    # Refers to login page
    return render_template('HTML/login.html')

@app.route('/api/countries', methods = ['GET'])
def countries():
    try:
        with open('countries.json') as f:
            countries_data = json.load(f)
        # return jsonify(countries_data)
        return jsonify(countries_data), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': f'Error in fetching countries: {str(e)}'}), 500

@app.route('/api/stock/chart', methods = ['POST'])
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



@app.route('/api/stock_info', methods=['POST'])
def stock_info():
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
        from dotenv import load_dotenv, find_dotenv
        import os
        _ = load_dotenv(find_dotenv())

        conn = psycopg2.connect(
            dbname = os.environ["PG_DB_NAME"],
            user = os.environ["PG_DB_USER"],
            password = os.environ["PG_DB_PSWD"],
            host = os.environ["PG_DB_IP"],
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

@app.route('/api/register', methods = ['POST'])
def register():

    required_keys = ['username','email','firstName','middleName','lastName','password']

    data = request.get_json()

    if not data:
        return jsonify({'isValid': False,'error': 'The form details is required'}), 400
        

    missing_keys = required_keys - data.keys()
    # print(missing_keys)
    if missing_keys:
        return jsonify({
            "errors": "All the required keys are missing"
        }), 400


    import psycopg2
    from psycopg2 import DatabaseError, IntegrityError
    try:
        from dotenv import load_dotenv, find_dotenv
        import os
        _ = load_dotenv(find_dotenv())

        conn = psycopg2.connect(
            dbname = os.environ["PG_DB_NAME"],
            user = os.environ["PG_DB_USER"],
            password = os.environ["PG_DB_PSWD"],
            host = os.environ["PG_DB_IP"],
            port = 5432
        )

        # Create a cursor
        cur = conn.cursor()
        query = """
            INSERT INTO postgres.public.users(email_id, username, password, first_name, middle_name, last_name)
            VALUES (%s,%s,%s,%s,%s,%s)
            returning id;
        """

        entry_tuple = (data['email'], data['username'], data['password'], data['firstName'], data['middleName'], data['lastName'], )

        cur.execute(query, entry_tuple)
        inserted_id = cur.fetchone()[0]
        
        conn.commit()

        return jsonify({"id", inserted_id, "errors", None}), 200
        
        
    except IntegrityError as e:
        # Handle Integrity Error
        conn.rollback()
        return jsonify({"errors": f"There was an integrity error in inserting registration form: {str(e)}"}), 500


    except DatabaseError as e:
        # Handle Database error
        conn.rollback()
        # print(str(e))
        return jsonify({"errors": f"There was a database error in inserting registration form: {str(e)}"}), 500
        
        
    except Exception as e:
        # All generic errors
        conn.rollback()
        return jsonify({"errors": f"There was an error in inserting registration form: {str(e)}"}), 500
        
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/api/login', methods = ['POST'])
def Login():
    """
    1st check 
    """
    data = request.get_json()
    print(data)

    if not data:
        return jsonify({ "success" : True, 'error': 'The username and Email id is required'}), 400

    if 'email' not in data.keys():
        return jsonify({ "success" : False, "error" : "The email is not present" }), 400
    email = data['email']

    if 'password' not in data.keys():
        return jsonify({ "success" : False, "error" : "The password is not present" }), 400
    password = data['password']

    import psycopg2
    from psycopg2 import DatabaseError, IntegrityError
    try:
        from dotenv import load_dotenv, find_dotenv
        import os
        _ = load_dotenv(find_dotenv())

        conn = psycopg2.connect(
            dbname = os.environ["PG_DB_NAME"],
            user = os.environ["PG_DB_USER"],
            password = os.environ["PG_DB_PSWD"],
            host = os.environ["PG_DB_IP"],
            port = 5432
        )

        # Create a cursor
        cur = conn.cursor()

        query = """
        SELECT
            password,
            id
        FROM
            postgres.public.users
        WHERE
            email_id = %s;
        
        """

        cur.execute(query, (email, ))

        pswd = cur.fetchone()
        print(pswd)
        cur.close()
        conn.close()

        if not pswd:
            # No email
            return jsonify({
                "success" : False,
                "error" : "EMAIL_NOT_FOUND",
                "message" : "Email not registered"
            }), 404
        if pswd[0] == password:
            # Password does match
            return jsonify({
                "success" : True,
                "error" : None,
                "message" : "Password matches",
                "token" : pswd[1]
            }), 200
        else:
            # Password does not match
            return jsonify({
                "success" : False,
                "error" : "INVALID_PASSWORD",
                "message" : "Invalid password"
            }), 401
    
    except Exception as e:
        return jsonify({
            "success" : False,
            "error" : "INTERNAL_SERVER_ERROR",
            "message" : "Internal Server Error"
        }), 500
    

if __name__ == '__main__':
    app.run(debug=True)
