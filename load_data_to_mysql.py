# -*- coding: utf-8 -*-
"""
4.3 DB 적재 및 검증
정제된 CSV들을 MySQL 테이블에 적재
  순서: dim_district(부모) -> dim_transport/fact_realestate(자식) / dim_income(독립)
"""

import pandas as pd
from sqlalchemy import create_engine, text

# ------------------------------------------------------------------
# 0. 접속 정보 (팀 환경에 맞게 수정)
# ------------------------------------------------------------------
DB_USER = "root"
DB_PASSWORD = "class1234"
DB_HOST = "localhost"
DB_NAME = "youth_housing_db"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
)

# ------------------------------------------------------------------
# 1. dim_district 적재 (refined_data.csv 에서 필요한 컬럼만 추출)
# ------------------------------------------------------------------
refined = pd.read_csv("final_refined_data.csv", encoding="utf-8-sig")

dim_district = refined[
    ["district", "youth_single_hh_total", "youth_population_total", "avg_area_m2_all_types"]
]
dim_district.to_sql("dim_district", engine, if_exists="append", index=False)
print(f"[완료] dim_district 적재: {len(dim_district)}행")

# ------------------------------------------------------------------
# 2. dim_transport 적재 (같은 refined_data.csv 에서 교통 관련 컬럼 추출)
# ------------------------------------------------------------------
dim_transport = refined[
    ["district", "rep_station",
     "time_to_gangnam_min", "time_to_gwanghwamun_min", "time_to_yeouido_min",
     "transfer_to_gangnam", "transfer_to_gwanghwamun", "transfer_to_yeouido"]
]
dim_transport.to_sql("dim_transport", engine, if_exists="append", index=False)
print(f"[완료] dim_transport 적재: {len(dim_transport)}행")

# ------------------------------------------------------------------
# 3. dim_income 적재 (독립 테이블, district 연결 없음)
# ------------------------------------------------------------------
income = pd.read_csv("05_income_avg_2024.csv", encoding="utf-8-sig")
income[["category", "item", "income_10k"]].to_sql(
    "dim_income", engine, if_exists="append", index=False
)
print(f"[완료] dim_income 적재: {len(income)}행")

# ------------------------------------------------------------------
# 4. fact_realestate 적재 (가장 큰 테이블, 개별 거래 단위)
# ------------------------------------------------------------------
real = pd.read_csv("01_realestate_for_analysis.csv", encoding="utf-8-sig")

fact_cols = ["district", "housing_type", "lease_type", "area_m2",
             "deposit_10k", "rent_10k", "deposit_flag",
             "rent_per_pyeong", "min_housing_flag"]

missing = [c for c in fact_cols if c not in real.columns]
if missing:
    print(f"[경고] 01_realestate_for_analysis.csv 에 다음 컬럼이 없습니다: {missing}")
    print("       -> 평당임대료(rent_per_pyeong), 최저주거기준(min_housing_flag) 컬럼을")
    print("          먼저 추가한 최신 버전 파일인지 확인하세요.")
else:
    real[fact_cols].to_sql(
        "fact_realestate", engine, if_exists="append", index=False, chunksize=5000
    )
    print(f"[완료] fact_realestate 적재: {len(real):,}행")

# ------------------------------------------------------------------
# 5. 적재 검증 (각 테이블 건수 확인)
# ------------------------------------------------------------------
print("\n=== 적재 검증 ===")
with engine.connect() as conn:
    for table in ["dim_district", "dim_transport", "dim_income", "fact_realestate"]:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f" - {table}: {count:,}행")

print("\nDB 적재 완료.")
