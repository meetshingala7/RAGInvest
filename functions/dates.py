from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

def calculate_dates(time_duration):
    today = date.today()

    if time_duration == "1D":
        return_time = today - timedelta(days = 1)
    
    elif time_duration == '5D':
        return_time = today - timedelta(days = 5)
    
    elif time_duration == '1M':
        return_time = today - relativedelta(months=1)
    
    elif time_duration == '3M':
        return_time = today - relativedelta(months=3)
    
    elif time_duration == '6M':
        return_time = today - relativedelta(months=6)
        
    elif time_duration == '1Y':
        return_time = today - relativedelta(years = 1)
        
    elif time_duration == '3Y':
        return_time = today - relativedelta(years = 3)
        
    else:
        return_time = today - relativedelta(years = 5)
        
    return today, return_time

if __name__ == "__main__":
    print(calculate_dates('1D'))
    print(calculate_dates('5D'))
    print(calculate_dates('1M'))
    print(calculate_dates('3M'))
    print(calculate_dates('6M'))
    print(calculate_dates('1Y'))
    print(calculate_dates('3Y'))
    print(calculate_dates('5Y'))
