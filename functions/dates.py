from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

def calculate_dates(time_duration):
    end_date = date.today()

    
    if time_duration == '5D':
        start_date = end_date - timedelta(days = 5)
    
    elif time_duration == '1M':
        start_date = end_date - relativedelta(months=1)
    
    elif time_duration == '3M':
        start_date = end_date - relativedelta(months=3)
    
    elif time_duration == '6M':
        start_date = end_date - relativedelta(months=6)
        
    elif time_duration == '1Y':
        start_date = end_date - relativedelta(years = 1)
        
    elif time_duration == '3Y':
        start_date = end_date - relativedelta(years = 3)
        
    else:
        start_date = end_date - relativedelta(years = 5)
        
    return end_date, start_date

if __name__ == "__main__":
    print(calculate_dates('5D'))
    print(calculate_dates('1M'))
    print(calculate_dates('3M'))
    print(calculate_dates('6M'))
    print(calculate_dates('1Y'))
    print(calculate_dates('3Y'))
    print(calculate_dates('5Y'))
