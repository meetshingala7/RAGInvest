def normalize_url(url):
    value = url.replace('\xa0', '.')
    value = value.replace(' ', '.')
    if value[:3] != 'www':
        value = 'https://www.' + value

    return value

if __name__ == "__main__":
    print(normalize_url("hdfcbank.com"))