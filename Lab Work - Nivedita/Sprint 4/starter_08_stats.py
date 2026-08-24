from pathlib import Path
import pandas as pd
from scipy import stats

DATA_PATH = Path(__file__).resolve().parents[2] / "shared" / "trades.csv"
df = pd.read_csv(DATA_PATH)

# TODO:
# 1. Calculate skew of quantity and value; comment on what each tells you about shape.
print(f"value skew: {df['value'].skew():.2f}")
print(f"quantity skew: {df['quantity'].skew():.2f}")

# 2. Calculate pearsonr(quantity, value); comment on r and p together.
r, p = stats.pearsonr(df["quantity"], df["price"])
print(f"\nquantity vs. price: r={r:.2f}, p={p:.2f}")

# 3. Discuss and comment: would a strong correlation here prove causation?

# 4. ttest_ind comparing BUY vs SELL value; interpret against 0.05, with a small-sample caveat.
buy_values = df.loc[df["side"] == "BUY", "value"]
sell_values = df.loc[df["side"] == "SELL", "value"]

t_stat, p_value = stats.ttest_ind(buy_values, sell_values, equal_var=False)
print(f"\nBUY mean: {buy_values.mean():,.2f}  SELL mean: {sell_values.mean():,.2f}")
print(f"t-test: t={t_stat:.2f}, p={p_value:.3f}")

if p_value < 0.05:
    print("p < 0.05: conventionally treated as evidence against the null hypothesis")
else:
    print("p >= 0.05: not enough evidence against the null hypothesis")

print(
    "Caution: this result sits close to the 0.05 line, and the SELL group has only 6 "
    "trades — a small sample like this deserves scepticism, not blind trust in the p-value."
)
