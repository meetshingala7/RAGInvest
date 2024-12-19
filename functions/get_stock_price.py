import requests
from bs4 import BeautifulSoup
from lxml import etree

# URL of the page to scrape
def stock_price(stock_label = 'HDFCBANK'):
    print(stock_label)
    if not stock_label:
        print('1')
        return {'code': 404, 'Stock Price':None}
    url = f"https://www.google.com/finance/quote/{stock_label}:NSE?hl=en"

    # Set headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    # Send GET request
    try:
        response = requests.get(url, headers=headers)
        
        # print(response.content)
        if response.status_code == 200:
            # Parse the HTML content
            # soup = BeautifulSoup(response.text, "html.parser")
            soup = BeautifulSoup(response.content,"lxml")

            # Attempt to find the element (this may not work for dynamic content)
            ele_stock_pirce = soup.find("div", class_="YMlKec fxKbKc")
            
            figure = soup.find_all("div", class_="P6K39c")
            names = soup.find_all("div", class_ = "mfs7Fc")
            # print(figure)
            # print(names)
            if ele_stock_pirce or figure or names:
                stock_price = ele_stock_pirce.text
                table_values = [{"name": names[i].text, "value": figure[i].text} for i in range(len(figure))]
                
                return {'code': 200, "Stock Price": stock_price, "table_values": table_values}
            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")
                return {'code': 310, "Stock Price": None}
    except Exception as e:
        print(e)
        return {'code': 403,"Stock Price": None}
