from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"

# TODO:
# 1. Load DATA_PATH into a DataFrame.
df = pd.read_csv(DATA_PATH)
print(f"df is a {type(df).__name__}")
# 2. Select SELL-only trades (trade_id, client_name, value) using .loc + boolean indexing.
print("\nSELL trades only (loc, condition-based):")
print(df.loc[df["side"] == "SELL", ["trade_id", "client_id", "value"]].head())
# 3. groupby("client_name")["value"].sum() and compare against your Module 3 totals.
print("\nTotal value by client name (pandas):")
print(df.groupby("client_name")["value"].sum())
# 4. df["advisor"].unique() for the distinct advisors.
print("\nDistinct Advisors:")
print(df["advisor"].unique())
# 5. Print a line-count comparison, and comment on what groupby is doing underneath.
print("\nLine-count comparison:")
print(f"Total rows in dataset: {len(df)}")
print(f"Sell Trades: {len(df.loc[df["side"] == "SELL"])}")
print(f"Distinct Advisors: len{df["advisor"].unique()}")
