from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# TODO:
# 1. Print df.shape and describe() on the numeric columns.
print(f"Shape: {df.shape}")
print("\ndescribe() on numeric columns:")
print(df[["quantity", "price", "value"]].describe())

# 2. Segment by currency: count and mean value per currency. Note the mixing anomaly.
print("\nValue by Currency")
print(df.groupby("currency")["value"].agg(["count", "mean"]))

# 3. Segment by client_name: highest total value, and highest trade count (may differ).
print("\nValue by Client_Name")
by_client_value = df.groupby("client_name")["value"].sum().sort_values(ascending=False)
print(by_client_value.head(3))

# 4. Segment by instrument, within asset_class == "Equity" only: highest total value.
equity = df[df["asset_class"]== "Equity"]
print(equity)
print(equity.groupby("instrument")["value"].sum().sort_values(ascending=True))

# 5. Write one pattern, one anomaly, and one specific, checkable hypothesis as comments.
# Pattern: Equity trades (11 of 20) outnumber every other asset class combined (9 of 20).
# Anomaly: value mixes USD and GBP without conversion (see currency segmentation above) —
#          any total or mean across the whole book is only meaningful within one currency.
# Hypothesis: clients served by J. Okafor (the advisor with the most trades) have a higher
#             mean trade value than clients served by the other two advisors — checkable
#             directly with df.groupby("advisor")["value"].mean(), and properly testable
#             with Module 8's statistical tools rather than eyeballing the means.
print("\nHypothesis check (mean value by advisor):")
print(df.groupby("advisor")["value"].mean().sort_values(ascending=False))
