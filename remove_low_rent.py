import pandas as pd

df = pd.read_csv("01_realestate_for_analysis.csv", encoding="utf-8-sig")

before = len(df)
mask_rent_low = df["rent_10k"] < 10
print(f"월세 10만원 미만 삭제 대상: {mask_rent_low.sum()}건")

df = df[~mask_rent_low]
after = len(df)
print(f"{before:,}행 -> {after:,}행 (제거율 {(before-after)/before*100:.3f}%)")

df.to_csv("01_realestate_for_analysis.csv", index=False, encoding="utf-8-sig")

# 재검증: 평당임대료 min값이 정상화됐는지 확인
print("\n=== 재검증: 평당임대료 통계 ===")
print(df["rent_per_pyeong"].describe())