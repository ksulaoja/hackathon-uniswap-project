from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import json

SECONDS_IN_HOUR = 3600


def query_pool_day_data(first, skip):
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    url = "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36"

    # Provide a GraphQL query
    queryPoolHourData = gql(
        """
        { poolDayDatas(first:%s, skip:%s, orderBy: date, orderDirection: desc, where: {
        pool: "%s" 
      } ) { 
        date
        token0Price
        token1Price
        feesUSD
        txCount
        open
        close
      } 

    } 
    """ % (first, skip, url)
    )

    # Execute the query on the transport
    result = client.execute(queryPoolHourData)
    return result


def query_pool_hour_data(first, skip):
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    url = "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36".lower()

    # Provide a GraphQL query
    queryPoolHourData = gql(
        """
        { poolHourDatas(first:%s, skip:%s, orderBy: periodStartUnix, orderDirection: desc, where: {
        pool: "%s" 
      } ) { 
        periodStartUnix
        token0Price
        token1Price
        open
        high
        low
        close
      } 
    } 
    """ % (first, skip, url)
    )

    return client.execute(queryPoolHourData)


def query_swaps(hourStartUnix, skip):
    hourEndUnix = hourStartUnix + SECONDS_IN_HOUR
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3")

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)

    url = "0x4e68ccd3e89f51c3074ca5072bbac773960dfa36".lower()

    # Provide a GraphQL query
    querySwaps = gql(
        """
        { swaps(first:1000, skip: %s ,orderBy: timestamp, orderDirection: asc, where: {
            pool: "%s"
            timestamp_gte: "%s"
            timestamp_lt: "%s"
        } ) {
            timestamp
            amount0 
            amount1
            }
        }
        """ % (skip, url, hourStartUnix, hourEndUnix)
    )

    return client.execute(querySwaps)


if __name__ == '__main__':
    result = query_pool_hour_data()["poolHourDatas"]
    poolHourDataByStartUnix = {}

    for poolData in result:
        poolHourDataByStartUnix[poolData["periodStartUnix"]] = poolData

    with open("data/pricebyhour.json", "w") as json_file:
        json.dump(result, json_file, indent=4)
    #print(query_swaps(1702069200))

