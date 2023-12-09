import requests

api_key = "dfb6ceae70764a048bcfeb228730cd2b"


def get_historical_prices(asset_base, asset_quote, time_start, time_end):
    url = f"https://api.twelvedata.com/time_series?symbol=ETH/BTC&interval=1h&apikey={api_key}&start_date={time_start}&end_date={time_end}"

    response = requests.request("GET", url)
    print(response.json().get("values"))
    return response.json()[0]


if __name__ == '__main__':
    get_historical_prices("ETH", "USD", "2023-12-09 10:00:00", "2023-12-09 10:59:59")