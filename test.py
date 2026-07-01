from vega_datasets import data
import pandas as pd

source = data.barley()

df = pd.DataFrame(source)

print(df)

