import requests

api_key = '8c2d7da176d4d306650ececa1964c901'
series_id = 'DGS10'


def get_compounded_risk_free_interest_rate():
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("observations")
        data_length = len(data)
        latest_value = data[data_length - 1].get("value")
        return float(latest_value) / 100
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return ""

if __name__ == '__main__':
    get_compounded_risk_free_interest_rate()