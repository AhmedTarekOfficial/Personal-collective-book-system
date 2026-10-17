import pandas as pd

df = pd.read_parquet("books_clean.parquet")

print(df["url"])
