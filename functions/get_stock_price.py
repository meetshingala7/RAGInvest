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
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        # Parse the HTML content
        # soup = BeautifulSoup(response.text, "html.parser")
        soup = BeautifulSoup(response.content,"lxml")

        # Use XPath to select the desired element
        # Attempt to find the element (this may not work for dynamic content)
        ele_stock_pirce = soup.find("div", class_="YMlKec fxKbKc")
        
        figure = soup.find_all("div", class_="P6K39c")
        names = soup.find_all("div", class_ = "mfs7Fc")
        
        if ele_stock_pirce or figure or names:
            stock_price = ele_stock_pirce.text
            figure = [i.text for i in figure]
            names = [i.text for i in names]

            return {'code': 200, "Stock Price": stock_price, "names": names, 'figure': figure}
        else:
            print("Failed to find the stock price. The content might be dynamically loaded.")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return {'code': response.status_code, "Stock Price": None}

