# -*- coding: utf-8 -*-
"""
4.2 테이블 생성 및 PK/FK
ERD(Fact_RealEstate - Dim_District/Dim_Transport/Dim_Income)를 그대로 MySQL 스키마로 생성
"""

import pymysql

# ------------------------------------------------------------------
# 0. 접속 정보 (팀 환경에 맞게 수정하세요)
# ------------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",       # MySQL 서버 주소 (보통 localhost)
    "user": "root",            # MySQL 계정
    "password": "class1234",
    "charset": "utf8mb4",
}
DB_NAME = "youth_housing_db"   # 프로젝트용 DB 이름 (원하는 이름으로 변경 가능)

# ------------------------------------------------------------------
# 1. DB 생성 (없으면 새로 만듦)
# ------------------------------------------------------------------
conn = pymysql.connect(**DB_CONFIG)
with conn.cursor() as cur:
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4")
conn.commit()
conn.close()
print(f"[완료] 데이터베이스 준비: {DB_NAME}")

# 이제부터는 해당 DB에 접속
DB_CONFIG["database"] = DB_NAME
conn = pymysql.connect(**DB_CONFIG)
cur = conn.cursor()

# ------------------------------------------------------------------
# 2. 차원 테이블(Dim) 먼저 생성 -> Fact 테이블의 FK가 참조할 대상이라 순서 중요
# ------------------------------------------------------------------

# 2-1. DIM_DISTRICT (자치구 차원)
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_district (
    district VARCHAR(10) NOT NULL,
    youth_single_hh_total INT,
    youth_population_total INT,
    avg_area_m2_all_types FLOAT,
    PRIMARY KEY (district)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")
print("[완료] dim_district 생성")

# 2-2. DIM_TRANSPORT (교통/거리 차원, district와 1:1)
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_transport (
    district VARCHAR(10) NOT NULL,
    rep_station VARCHAR(20),
    time_to_gangnam_min INT,
    time_to_gwanghwamun_min INT,
    time_to_yeouido_min INT,
    transfer_to_gangnam INT,
    transfer_to_gwanghwamun INT,
    transfer_to_yeouido INT,
    PRIMARY KEY (district),
    FOREIGN KEY (district) REFERENCES dim_district(district)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")
print("[완료] dim_transport 생성")

# 2-3. DIM_INCOME (소득 참조 테이블, 구별 연결 없는 독립 테이블)
cur.execute("""
CREATE TABLE IF NOT EXISTS dim_income (
    income_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(20),
    item VARCHAR(20),
    income_10k INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")
print("[완료] dim_income 생성")

# ------------------------------------------------------------------
# 3. 팩트 테이블(Fact) 생성 -> dim_district를 FK로 참조
# ------------------------------------------------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS fact_realestate (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    district VARCHAR(10) NOT NULL,
    housing_type VARCHAR(20),
    lease_type VARCHAR(10),
    area_m2 FLOAT,
    deposit_10k INT,
    rent_10k INT,
    deposit_flag VARCHAR(10),
    rent_per_pyeong FLOAT,
    min_housing_flag VARCHAR(10),
    FOREIGN KEY (district) REFERENCES dim_district(district)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
""")
print("[완료] fact_realestate 생성")

conn.commit()

# ------------------------------------------------------------------
# 4. 생성된 테이블 목록 확인
# ------------------------------------------------------------------
cur.execute("SHOW TABLES;")
tables = cur.fetchall()
print("\n[생성된 테이블 목록]")
for t in tables:
    print(" -", t[0])

cur.close()
conn.close()
print("\n스키마 구축 완료.")
