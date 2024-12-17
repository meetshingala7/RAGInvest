import requests
from bs4 import BeautifulSoup
from lxml import etree

# URL of the page to scrape
def previous_close(stock_label = 'HDFCBANK'):
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
        figure = soup.find_all("div", class_="P6K39c")
        figure = [i.text for i in figure]
        names = soup.find_all("div", class_ = "mfs7Fc")
        names = [i.text for i in names]
        
        print(figure)
        print(names)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return {'code': response.status_code, "Stock Price": None}

previous_close()