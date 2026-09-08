# -*- coding: utf-8 -*-
"""
6개 정제 파일의 컬럼명을 영문으로 표준화
  - '자치구/자치구명/구' -> 전부 'district' 로 통일 (merge 키 일치시키기 위함)
"""

import pandas as pd

BASE = "/mnt/user-data/uploads/"
OUT_DIR = "/mnt/user-data/outputs/"

rename_maps = {
    "01_realestate_for_analysis.csv": {
        "NO": "id",
        "자치구": "district",
        "시군구": "full_address",
        "전월세구분": "lease_type",
        "전용면적_㎡": "area_m2",
        "보증금_만원": "deposit_10k",
        "월세금_만원": "rent_10k",
        "보증금유무": "deposit_flag",
        "주택유형": "housing_type",
    },
    "02_seoul_youth_households.csv": {
        "자치구": "district",
        "청년_1인가구수_총합": "youth_single_hh_total",
        "20~24세": "age_20_24",
        "25~29세": "age_25_29",
        "30~34세": "age_30_34",
        "35~39세": "age_35_39",
    },
    "03_youth_population_2026.csv": {
        "자치구": "district",
        "20~24세": "age_20_24",
        "25~29세": "age_25_29",
        "30~34세": "age_30_34",
        "35~39세": "age_35_39",
    },
    "04_seoul_monthly_rent_area_summary.csv": {
        "자치구명": "district",
        "건물용도": "housing_type",
        "평균_임대면적_m2": "avg_area_m2",
        "월세_거래건수": "rent_txn_count",
    },
    "05_income_avg_2024.csv": {
        "구분": "category",
        "세부항목": "item",
        "연소득_만원": "income_10k",
    },
    "06_distance_wide.csv": {
        "구": "district",
        "대표역": "rep_station",
        "강남역_소요시간(분)": "time_to_gangnam_min",
        "광화문역_소요시간(분)": "time_to_gwanghwamun_min",
        "여의도역_소요시간(분)": "time_to_yeouido_min",
        "강남역_환승횟수": "transfer_to_gangnam",
        "광화문역_환승횟수": "transfer_to_gwanghwamun",
        "여의도역_환승횟수": "transfer_to_yeouido",
    },
}

encodings_try = ["utf-8", "utf-8-sig", "cp949"]

for filename, colmap in rename_maps.items():
    df = None
    for enc in encodings_try:
        try:
            df = pd.read_csv(BASE + filename, encoding=enc, low_memory=False)
            break
        except Exception:
            continue
    if df is None:
        print(f"[실패] {filename} 못 읽음")
        continue

    before_cols = list(df.columns)
    df = df.rename(columns=colmap)

    out_name = filename  # 파일명은 그대로, 컬럼명만 변경
    df.to_csv(OUT_DIR + out_name, index=False, encoding="utf-8-sig")

    print(f"[{filename}]")
    print("  before:", before_cols)
    print("  after :", list(df.columns))
    print()

print("전체 완료. /mnt/user-data/outputs/ 에 컬럼명 영문화된 파일 저장됨.")
