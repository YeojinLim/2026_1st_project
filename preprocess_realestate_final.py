# -*- coding: utf-8 -*-
"""
2025-08-01~2026-07-31 주택유형별(월세) 실거래가 전처리
기준:
  1) 월세금 0원 이하        -> 삭제
  2) 보증금 0원 이하        -> 삭제하지 않고 '보증금유무' 컬럼 추가(무보증/보증금있음)
  3) 전용면적 130㎡ 초과      -> 삭제
  4) 보증금 5억원 이상       -> 분석용 컬럼에서는 제외, 원본은 별도 보관 + 건수 기록
"""

import pandas as pd

RAW_PATH = r"C:\Users\user\Desktop\csv 파일\1. 2025-08-01 ~ 2026-07-31 주택유형별(월세)_실거래가.csv"
OUT_DIR = r"C:\Users\user\Desktop\csv 파일\\"

SEOUL_GU_LIST = [
    "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구",
    "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", "강서구",
    "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구",
]


def extract_gu(text: str):
    if not isinstance(text, str):
        return None
    for gu in SEOUL_GU_LIST:
        if gu in text:
            return gu
    return None


# ------------------------------------------------------------------
# 0. 데이터 로드 + 기본 정리
# ------------------------------------------------------------------
df = pd.read_csv(RAW_PATH, encoding="cp949", low_memory=False)
print(f"[원본] 총 {len(df):,}행")

df["자치구"] = df["시군구"].apply(extract_gu)

# 금액 컬럼 숫자화 (쉼표 제거)
df["보증금_만원"] = pd.to_numeric(
    df["보증금(만원)"].astype(str).str.replace(",", "", regex=False), errors="coerce"
)
df["월세금_만원"] = pd.to_numeric(
    df["월세금(만원)"].astype(str).str.replace(",", "", regex=False), errors="coerce"
)
df["전용면적_㎡"] = pd.to_numeric(df["전용면적(㎡)"], errors="coerce")

# ------------------------------------------------------------------
# 1. 월세금 0원 이하 -> 삭제
# ------------------------------------------------------------------
before = len(df)
mask_rent_zero = df["월세금_만원"] <= 0
print(f"[기준1] 월세금 0원 이하: {mask_rent_zero.sum()}건 삭제")
df = df[~mask_rent_zero]

# ------------------------------------------------------------------
# 2. 보증금 0원 이하 -> 삭제 대신 '보증금유무' 컬럼 추가
# ------------------------------------------------------------------
df["보증금유무"] = df["보증금_만원"].apply(lambda x: "무보증" if x == 0 else "보증금있음")
print(f"[기준2] 무보증(보증금 0원) 건수: {(df['보증금유무']=='무보증').sum()}건 -> 삭제하지 않고 컬럼으로 표시")

# ------------------------------------------------------------------
# 3. 전용면적 130㎡ 초과 -> 삭제
# ------------------------------------------------------------------
mask_area_over = df["전용면적_㎡"] > 130
print(f"[기준3] 전용면적 130㎡ 초과: {mask_area_over.sum()}건 삭제")
df = df[~mask_area_over]

# ------------------------------------------------------------------
# 4. 보증금 5억(=50,000만원) 이상 -> 분석용에서는 제외, 원본은 별도 보관
# ------------------------------------------------------------------
mask_deposit_high = df["보증금_만원"] >= 50000
n_high = mask_deposit_high.sum()
print(f"[기준4] 보증금 5억 이상: {n_high}건 -> 고가매물 별도 저장, 분석용에서는 제외")

high_price = df[mask_deposit_high].copy()          # 원본 보관용
df_for_analysis = df[~mask_deposit_high].copy()    # 분석용 (고가매물 제외)

after = len(df_for_analysis)
print(f"\n[정제 결과] {before:,}행 -> 분석용 {after:,}행 (고가매물 {n_high}건 별도 보관)")

# ------------------------------------------------------------------
# 저장
# ------------------------------------------------------------------
final_cols = ["NO", "자치구", "시군구", "전월세구분", "전용면적_㎡",
              "보증금_만원", "월세금_만원", "보증금유무", "주택유형"]

df_for_analysis[final_cols].to_csv(
    OUT_DIR + "cleaned_realestate_for_analysis.csv", index=False, encoding="utf-8-sig"
)
high_price[final_cols].to_csv(
    OUT_DIR + "cleaned_realestate_highprice_excluded.csv", index=False, encoding="utf-8-sig"
)

print("\n[저장 완료]")
print(" - cleaned_realestate_for_analysis.csv   (분석용, 고가매물 제외)")
print(" - cleaned_realestate_highprice_excluded.csv  (제외된 고가매물 원본 보관)")

# 구별 x 주택유형별 요약 미리보기
summary = (
    df_for_analysis.groupby(["자치구", "주택유형"])
    .agg(평균월세=("월세금_만원", "mean"),
         평균보증금=("보증금_만원", "mean"),
         평균면적=("전용면적_㎡", "mean"),
         무보증건수=("보증금유무", lambda x: (x == "무보증").sum()),
         건수=("월세금_만원", "count"))
    .round(1)
)
print("\n[구별 x 주택유형별 요약 미리보기]")
print(summary.head(10))
