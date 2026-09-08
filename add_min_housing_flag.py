import pandas as pd

df = pd.read_csv("01_realestate_for_analysis.csv", encoding="utf-8-sig")

# 면적 층화 (14㎡ 최저주거기준)
df["min_housing_flag"] = df["area_m2"].apply(
    lambda x: "기준미달" if x < 14 else "기준충족"
)

# 확인
print(df["min_housing_flag"].value_counts())
print(df[["district", "housing_type", "area_m2", "min_housing_flag"]].head())

df.to_csv("01_realestate_for_analysis.csv", index=False, encoding="utf-8-sig")