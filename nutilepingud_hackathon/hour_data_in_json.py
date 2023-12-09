import time
from api.queries import *
SECONDS_IN_HOUR = 3600

def do_stuff(output_file):
    start_time = time.time()
    poolHourData = query_pool_hour_data(1000, 0)["poolHourDatas"]
    poolHourDataByStartUnix = {}

    for poolData in poolHourData:
        poolHourDataByStartUnix[poolData["periodStartUnix"]] = poolData

    swapsByStartUnix = {}
    skip = 0

    counter = 1
    for hourStartUnix in poolHourDataByStartUnix:
        swapsByStartUnix[hourStartUnix] = {}
        swapsByStartUnix[hourStartUnix]["priceEth"] = poolHourDataByStartUnix[hourStartUnix]["token1Price"]
        swapsByStartUnix[hourStartUnix]["priceUsdt"] = poolHourDataByStartUnix[hourStartUnix]["token0Price"]
        swapsByStartUnix[hourStartUnix]["open"] = poolHourDataByStartUnix[hourStartUnix]["open"]
        swapsByStartUnix[hourStartUnix]["high"] = poolHourDataByStartUnix[hourStartUnix]["high"]
        swapsByStartUnix[hourStartUnix]["low"] = poolHourDataByStartUnix[hourStartUnix]["low"]
        swapsByStartUnix[hourStartUnix]["close"] = poolHourDataByStartUnix[hourStartUnix]["close"]
        print(counter)
        counter += 1
        for i in range(4):
            swaps = query_swaps(hourStartUnix, skip)["swaps"]
            if "swaps" in swapsByStartUnix[hourStartUnix]:
                swapsByStartUnix[hourStartUnix]["swaps"].extend(swaps)
            else:
                swapsByStartUnix[hourStartUnix]["swaps"] = swaps
            skip += 1000
        skip = 0

    with open(output_file, "w") as json_file:
        json.dump(swapsByStartUnix, json_file, indent=4)

    print(swapsByStartUnix)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print(f"My function took {elapsed_time} seconds to execute.")


if __name__ == '__main__':
    do_stuff("data/hourData.json")
