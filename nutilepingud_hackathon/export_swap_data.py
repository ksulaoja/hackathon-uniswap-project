import json, datetime
from tools.csv_writer import *

def export_swap_data(filename):
    exportArray = []

    # Open the file in read mode
    with open(filename, "r") as json_file:
        # Load the JSON data
        data = json.load(json_file)

        for hourUnix in data.keys():
            exportArray.append(hour_data_to_csv_array_element(data[hourUnix], hourUnix))

    write_to_csv(exportArray, "data/toExcel.csv")


def hour_data_to_csv_array_element(data, hour_unix):
    hour_data = {}
    dt = datetime.datetime.fromtimestamp(int(hour_unix))
    hour_data["date"] = dt.date()
    hour_data["time"] = dt.time()
    hour_data["priceEth"] = data["priceEth"]
    hour_data["priceUsdt"] = data["priceUsdt"]

    buy_eth_counter = 0
    sell_eth_counter = 0

    buy_eth_amount = 0
    sell_eth_amount = 0

    buy_usdt_counter = 0
    sell_usdt_counter = 0

    buy_usdt_amount = 0
    sell_usdt_amount = 0

    for swap in data["swaps"]:
        eth_amount = swap["amount0"]
        usdt_amount = swap["amount1"]
        if float(eth_amount) > 0:
            buy_eth_counter += 1
            sell_usdt_counter += 1

            buy_eth_amount += float(eth_amount)
            sell_usdt_amount += abs(float(usdt_amount))
        else:
            sell_eth_counter += 1
            buy_usdt_counter += 1

            sell_eth_amount += float(eth_amount)
            buy_usdt_amount += abs(float(usdt_amount))

    hour_data["buyEthCounter"] = buy_eth_counter
    hour_data["sellEthCounter"] = sell_eth_counter

    hour_data["buyEthAmount"] = buy_eth_amount
    hour_data["sellEthAmount"] = sell_eth_amount

    hour_data["buyUsdtCounter"] = buy_usdt_counter
    hour_data["sellUsdtCounter"] = sell_usdt_counter

    hour_data["buyUsdtAmount"] = buy_usdt_amount
    hour_data["sellUsdtAmount"] = sell_usdt_amount

    return hour_data


if __name__ == '__main__':
    export_swap_data("data/hourData.json")

