import yfinance as yf
import pandas as pd
import os


def download_and_store_data(stock_symbol = 'RELIANCE', start_date = '2020-01-01', end_date = "2024-12-16"):
    stock_symbol = stock_symbol.upper()
    stock_symbol = f'{stock_symbol}.NS'
    # Fetch historical data

    directory_path = 'charting_functions/Data'
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = f'{stock_symbol}{start_date}{end_date}.parquet'
    full_path = f'{directory_path}/{file_path}'

    if not os.path.isfile(full_path):
        data = yf.download(stock_symbol, start = start_date, end = end_date)
        data.to_parquet(full_path)
    
    return full_path
    
    

if __name__ == "__main__":
    print(download_data(stock_symbol = 'HDFCBANK'))