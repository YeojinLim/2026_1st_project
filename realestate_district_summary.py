import pandas as pd

df = pd.read_csv("01_realestate_for_analysis.csv", encoding="utf-8-sig")

# 구별 x 주택유형별 집계
summary = (
    df.groupby(["district", "housing_type"])
    .agg(
        avg_rent=("rent_10k", "mean"),
        avg_deposit=("deposit_10k", "mean"),
        avg_area=("area_m2", "mean"),
        avg_rent_per_pyeong=("rent_per_pyeong", "mean"),
        min_housing_ratio=("min_housing_flag", lambda x: (x=="기준미달").mean()),
        no_deposit_count=("deposit_flag", lambda x: (x=="무보증").sum()),
        txn_count=("rent_10k", "count"),
    )
    .round(2)
    .reset_index()
)

print(summary.head(10))
print(f"\n총 {len(summary)}행 (구 25개 x 주택유형 3종 = 최대 75행)")

summary.to_csv("10_realestate_district_summary.csv", index=False, encoding="utf-8-sig")
print("\n저장 완료: 10_realestate_district_summary.csv")