from scipy.stats import norm
import math

from api.etherum_price import get_etherum_price
from api.fred import get_compounded_risk_free_interest_rate


def black_sholes():
    stock_price = get_etherum_price()
    ex_price = stock_price  # Exercise price of Option
    t = 23.791  # Numer of periods to Exercise in years
    rf = get_compounded_risk_free_interest_rate()  # Compounded Risk-Free Interest Rate
    s = 1.2  # Standard Deviation. 120% as a decimal

    d1 = (math.log(stock_price / ex_price) + (rf + (s ** 2) / 2) * t) / (s * (t ** 0.5))

    print(d1)

    # Calculate the cumulative distribution function (CDF) of the standard normal distribution
    result_normdist = norm.cdf(d1, 0, 1)

    print(result_normdist)


if __name__ == '__main__':
    black_sholes()