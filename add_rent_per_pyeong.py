import pandas as pd

df = pd.read_csv("01_realestate_for_analysis.csv", encoding="utf-8-sig")

# 1) 평수 계산 (1평 = 3.3058㎡)
df["area_pyeong"] = df["area_m2"] / 3.3058

# 2) 평당임대료 계산 (만원/평)
df["rent_per_pyeong"] = df["rent_10k"] / df["area_pyeong"]

# 확인
print(df[["district", "housing_type", "area_m2", "area_pyeong", "rent_10k", "rent_per_pyeong"]].head())
print(df["rent_per_pyeong"].describe())

df.to_csv("01_realestate_for_analysis.csv", index=False, encoding="utf-8-sig")