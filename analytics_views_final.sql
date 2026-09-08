-- 5.5 Power BI 연동용 View 작성 (최종 확정 KPI 5개 반영)
-- Power BI에서는 이 5개 View를 테이블처럼 그대로 불러오면 됨

-- KPI 1: 소득 대비 임대료 비율 (RIR)
-- 공식: (구별 평균 월세 / 서울시 청년 1인 가구 월평균 소득) * 100
CREATE OR REPLACE VIEW view_kpi1_rir AS
WITH monthly_income AS (
    SELECT income_10k / 12 AS monthly_income_10k
    FROM dim_income
    WHERE item = '서울'
)
SELECT
    f.district AS district,
    ROUND(AVG(f.rent_10k), 1) AS avg_rent_10k,
    ROUND((SELECT monthly_income_10k FROM monthly_income), 1) AS monthly_income_10k,
    ROUND(AVG(f.rent_10k) / (SELECT monthly_income_10k FROM monthly_income) * 100, 2) AS rir_pct,
    COUNT(*) AS txn_count
FROM fact_realestate f
GROUP BY f.district;


-- KPI 2: 평당 임대료
-- 공식: 구별 평균 월세 / 구별 평균 전용면적(평)
CREATE OR REPLACE VIEW view_kpi2_rent_per_pyeong AS
SELECT
    f.district AS district,
    ROUND(AVG(f.rent_10k), 1) AS avg_rent_10k,
    ROUND(AVG(f.area_m2) / 3.3058, 2) AS avg_area_pyeong,
    ROUND(AVG(f.rent_10k) / (AVG(f.area_m2) / 3.3058), 1) AS rent_per_pyeong_10k,
    COUNT(*) AS txn_count
FROM fact_realestate f
GROUP BY f.district;


-- KPI 3: 주거 가성비 지수
-- 공식: (평균 전용면적 / (RIR * 업무지구 평균 소요시간)) * 10,000
CREATE OR REPLACE VIEW view_kpi3_housing_efficiency AS
WITH district_base AS (
    SELECT
        f.district,
        AVG(f.rent_10k) AS avg_rent,
        AVG(f.area_m2) AS avg_area_m2,
        (t.time_to_gangnam_min + t.time_to_gwanghwamun_min + t.time_to_yeouido_min) / 3 AS avg_commute
    FROM fact_realestate f
    JOIN dim_transport t ON f.district = t.district
    GROUP BY f.district, avg_commute
),
monthly_income AS (
    SELECT income_10k / 12 AS monthly_income_10k
    FROM dim_income
    WHERE item = '서울'
)
SELECT
    d.district AS district,
    ROUND(d.avg_area_m2, 1) AS avg_area_m2,
    ROUND(d.avg_rent / m.monthly_income_10k * 100, 2) AS rir_pct,
    ROUND(d.avg_commute, 1) AS avg_commute_min,
    ROUND(
        (d.avg_area_m2 / ((d.avg_rent / m.monthly_income_10k * 100) * d.avg_commute)) * 10000
    , 2) AS housing_efficiency_index
FROM district_base d
CROSS JOIN monthly_income m;


-- KPI 4: 시간당 월세 기회비용
-- 공식: Δ월세(만원) / Δ출퇴근 소요시간(10분 단위)
-- 구 1개로는 변화량 계산 불가 -> 25개 구 회귀분석으로 서울 전체 기준 1개 값 산출
CREATE OR REPLACE VIEW view_kpi4_time_opportunity_cost AS
WITH district_base AS (
    SELECT
        f.district,
        AVG(f.rent_10k) AS avg_rent,
        (t.time_to_gangnam_min + t.time_to_gwanghwamun_min + t.time_to_yeouido_min) / 3 AS avg_commute
    FROM fact_realestate f
    JOIN dim_transport t ON f.district = t.district
    GROUP BY f.district, avg_commute
)
SELECT
    ROUND(
        (AVG(avg_commute * avg_rent) - AVG(avg_commute) * AVG(avg_rent)) / VAR_POP(avg_commute)
    , 3) AS slope_10k_per_min,
    ROUND(
        10 * ((AVG(avg_commute * avg_rent) - AVG(avg_commute) * AVG(avg_rent)) / VAR_POP(avg_commute))
    , 2) AS time_opportunity_cost_per_10min_10k
FROM district_base;


-- KPI 5: 최저 주거기준 충족률
-- 공식: (구별 평균 전용면적(㎡) / 14㎡) * 100
CREATE OR REPLACE VIEW view_kpi5_min_housing_ratio AS
SELECT
    f.district AS district,
    ROUND(AVG(f.area_m2), 2) AS avg_area_m2,
    ROUND(AVG(f.area_m2) / 14 * 100, 1) AS min_housing_ratio_pct,
    COUNT(*) AS txn_count
FROM fact_realestate f
GROUP BY f.district;


-- 생성 확인
SHOW FULL TABLES WHERE Table_type = 'VIEW';
