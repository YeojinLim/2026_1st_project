-- KPI 5: 최저 주거기준 충족률
-- 공식: (구별 평균 전용면적(㎡) / 14㎡) * 100

SELECT
    f.district AS 자치구,
    ROUND(AVG(f.area_m2), 2) AS 평균전용면적_m2,
    ROUND(AVG(f.area_m2) / 14 * 100, 1) AS KPI5_최저주거기준충족률_퍼센트,
    COUNT(*) AS 거래건수
FROM fact_realestate f
GROUP BY f.district
ORDER BY KPI5_최저주거기준충족률_퍼센트 ASC;
