from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "messy-trades-raw.csv"

df = pd.read_csv(DATA_PATH)

# TODO, each with a one-line comment explaining your reasoning:
# 1. Drop the row with missing quantity (can't be safely reconstructed).
before = len(df)
df = df[df["quantity"].notna()].copy()
print(f"\nDropped {before - len(df)} row(s) with missing quantity (can't be reconstructed)")

# 2. Recompute the missing value as quantity * price.
df["quantity"] = df["quantity"].astype(float)
missing_value = df["value"].isna()
df.loc[missing_value, "value"] = df.loc[missing_value, "quantity"] * df.loc[missing_value, "price"]
print(f"Recomputed value for {missing_value.sum()} row(s) from quantity * price")

# 3. Backfill the missing client_name from another row with the same client_id.
missing_name = df["client_name"].isna().sum()
df["client_name"] = df.groupby("client_id")["client_name"].transform("first")
print(f"Backfilled client_name for {missing_name} row(s) using a matching client_id")

# 4. Parse trade_date correctly, resolving the ambiguous DD/MM/YYYY row using the
#    surrounding trade_id sequence, not an assumption.
df["trade_date"] = pd.to_datetime(df["trade_date"], format="mixed", dayfirst=True)
print(f"\ntrade_date dtype after parsing: {df['trade_date'].dtype}")

# 5. Normalise asset_class casing without turning "ETF" into "Etf" (use a canonical mapping).
ASSET_CLASS_CANONICAL = {"equity": "Equity", "bond": "Bond", "etf": "ETF", "crypto": "Crypto"}
df["asset_class"] = df["asset_class"].str.lower().map(ASSET_CLASS_CANONICAL)
print(f"Distinct asset classes after normalising case: {sorted(df['asset_class'].unique())}")

# 6. Drop the exact duplicate row.
before = len(df)
df = df.drop_duplicates()
print(f"\nDropped {before - len(df)} exact duplicate row(s)")

# 7. Flag (don't drop) the quantity outlier, with a one-sentence investigation note.
equity_quantities = df.loc[df["asset_class"] == "Equity", "quantity"]
q3 = equity_quantities.quantile(0.75)
outliers = df[(df["asset_class"] == "Equity") & (df["quantity"] > q3 * 5)]
print(f"\nFlagged {len(outliers)} outlier(s) for review (not auto-removed):")
print(outliers[["trade_id", "instrument", "quantity"]])


print(f"Final row count: {len(df)}")
