-- KPI 2: 평당 임대료
-- 공식: 구별 평균 월세 / 구별 평균 전용면적(평)

SELECT
    f.district AS 자치구,
    ROUND(AVG(f.rent_10k), 1) AS 평균월세_만원,
    ROUND(AVG(f.area_m2) / 3.3058, 2) AS 평균전용면적_평,
    ROUND(
        AVG(f.rent_10k) / (AVG(f.area_m2) / 3.3058)
    , 1) AS KPI2_평당임대료_만원,
    COUNT(*) AS 거래건수
FROM fact_realestate f
GROUP BY f.district
ORDER BY KPI2_평당임대료_만원 DESC;
