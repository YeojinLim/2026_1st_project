-- KPI 3: 주거가성비지수
-- 공식: (평균 전용면적 / (RIR * 업무지구 평균 소요시간)) * 10,000

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
    d.district AS 자치구,
    ROUND(d.avg_area_m2, 1) AS 평균전용면적_m2,
    ROUND(d.avg_rent / m.monthly_income_10k * 100, 2) AS RIR_퍼센트,
    ROUND(d.avg_commute, 1) AS 평균통근시간_분,
    ROUND(
        (d.avg_area_m2 / ((d.avg_rent / m.monthly_income_10k * 100) * d.avg_commute)) * 10000
    , 2) AS 주거가성비지수
FROM district_base d
CROSS JOIN monthly_income m
ORDER BY 주거가성비지수 DESC;
