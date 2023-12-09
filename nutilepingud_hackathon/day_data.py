from api import queries
from tools import csv_writer
from datetime import datetime


def day_data():
    day_data = queries.query_pool_day_data(1000, 0)["poolDayDatas"]
    print(day_data)
    result = []
    for day in day_data:
        day_object = {"date": datetime.fromtimestamp(day["date"]).date(),
                      "ethPrice": day["token1Price"],
                      "usdtPrice": day["token0Price"],
                      "feesUSD": day["feesUSD"],
                      "txCount": day["txCount"],
                      "open": day["open"],
                      "close": day["close"]}
        result.append(day_object)
    csv_writer.write_to_csv(result, "data/day_data.csv")


if __name__ == '__main__':
    day_data()
