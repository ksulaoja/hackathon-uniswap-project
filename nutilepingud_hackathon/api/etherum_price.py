import requests

def get_etherum_price():
    url = "https://api.coinbase.com/v2/prices/ETH-USD/buy"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data")
        price = data.get("amount")
        return float(price)
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return ""


if __name__ == '__main__':
    get_etherum_price()