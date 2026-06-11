

import pandas as pd
from vega_datasets import data


def get_data():
    source = data.stocks()
    source = source[source.date.gt("2004-01-01")]
    return source

stock_data = get_data()

print(stock_data)