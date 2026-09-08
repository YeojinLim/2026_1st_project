-- KPI 1: 소득 대비 임대료 비율 (RIR)
-- 공식: (구별 평균 월세 / 서울시 청년 1인 가구 월평균 소득) * 100
-- [주의] 원 공식엔 '평균 관리비'도 포함되나, 수집 데이터에 관리비 항목이 없어 월세만으로 산출

WITH monthly_income AS (
    -- 서울 청년 개인 연소득(2,722만원) -> 12로 나눠서 월평균소득으로 환산
    SELECT income_10k / 12 AS monthly_income_10k
    FROM dim_income
    WHERE item = '서울'
)
SELECT
    f.district AS 자치구,
    ROUND(AVG(f.rent_10k), 1) AS 평균월세_만원,
    ROUND((SELECT monthly_income_10k FROM monthly_income), 1) AS 월평균소득_만원,
    ROUND(
        AVG(f.rent_10k) / (SELECT monthly_income_10k FROM monthly_income) * 100
    , 2) AS KPI1_RIR_퍼센트,
    COUNT(*) AS 거래건수
FROM fact_realestate f
GROUP BY f.district
ORDER BY KPI1_RIR_퍼센트 DESC;
