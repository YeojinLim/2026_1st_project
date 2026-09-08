-- KPI 4: 시간당 월세 기회비용
-- 공식: Δ월세(만원) / Δ출퇴근 소요시간(10분 단위)
-- 구 1개만으로는 '변화량(Δ)'을 계산할 수 없어서, 25개 구 데이터로 회귀직선을 구하고
-- 그 기울기를 10분 단위로 환산해서 "서울 전체 기준 1개 값"으로 산출함

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
    , 3) AS 기울기_만원per1분,
    ROUND(
        10 * (
            (AVG(avg_commute * avg_rent) - AVG(avg_commute) * AVG(avg_rent)) / VAR_POP(avg_commute)
        )
    , 2) AS KPI4_시간당월세기회비용_10분당_만원
FROM district_base;
