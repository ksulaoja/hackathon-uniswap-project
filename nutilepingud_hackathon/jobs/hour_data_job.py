import csv
import time
import schedule
from datetime import datetime

from api.coinapi import get_historical_prices
from api.queries import query_pool_hour_data, query_swaps


def get_hour_data():
    pool_hour_data = query_pool_hour_data(1, 1)["poolHourDatas"][0]
    hour_start_unix = pool_hour_data["periodStartUnix"]
    swaps = []
    skip = 0

    resultRow = []

    resultRow.append(datetime.fromtimestamp(hour_start_unix).date())
    resultRow.append(datetime.fromtimestamp(hour_start_unix).time())
    resultRow.append(pool_hour_data["token1Price"])
    resultRow.append(pool_hour_data["token0Price"])
    resultRow.append(pool_hour_data["open"])
    resultRow.append(pool_hour_data["close"])
    resultRow.append(pool_hour_data["high"])
    resultRow.append(pool_hour_data["low"])

    for i in range(4):
        queried_swaps = query_swaps(hour_start_unix, skip)["swaps"]
        print(queried_swaps)
        if len(queried_swaps) > 0:
            if len(swaps) > 0:
                swaps.extend(queried_swaps)
            else:
                swaps = queried_swaps
            print(swaps)
            skip += 1000
        else:
            break

    buy_eth_counter = 0
    sell_eth_counter = 0

    buy_eth_amount = 0
    sell_eth_amount = 0

    buy_usdt_counter = 0
    sell_usdt_counter = 0

    buy_usdt_amount = 0
    sell_usdt_amount = 0

    for swap in swaps:
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

    resultRow.append(buy_eth_counter)
    resultRow.append(sell_eth_counter)

    resultRow.append(buy_eth_amount)
    resultRow.append(sell_eth_amount)

    resultRow.append(buy_usdt_counter)
    resultRow.append(sell_usdt_counter)

    resultRow.append(buy_usdt_amount)
    resultRow.append(sell_usdt_amount)

    with open("../data/toExcel.csv", mode='a', newline='') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)
        # Write the new data as a new row
        csv_writer.writerow(resultRow)


def get_eth_usd_price_rates():
    current_time = datetime.now()
    rounded_time = current_time.replace(minute=0, second=0, microsecond=0)

    historical_prices = get_historical_prices("ETH", "USD", "2023-12-09T10:00:00.000Z", "2023-12-09T11:00:00.000Z")


def update_hour_data():
    schedule.every().hour.at(":00").do(get_hour_data)
    schedule.every().hour.at(":00").do(get_eth_usd_price_rates)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    get_hour_data()
    #schedule.every().hour.at(":00").do(get_hour_data)

    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
