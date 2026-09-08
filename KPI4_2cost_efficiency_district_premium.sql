-- 5.2-3 구별 "직주근접 프리미엄/할인" 조회
-- 서울 전체 회귀식(월세 = 기울기*통근시간 + 절편)으로 예측한 월세와
-- 실제 평균월세를 비교해, 각 구가 그 공식보다 비싼지/싼지 보여줌

WITH district_stats AS (
    SELECT
        f.district,
        AVG(f.rent_10k) AS avg_rent,
        (t.time_to_gangnam_min + t.time_to_gwanghwamun_min + t.time_to_yeouido_min) / 3 AS avg_commute
    FROM fact_realestate f
    JOIN dim_transport t ON f.district = t.district
    GROUP BY f.district, avg_commute
),
city_regression AS (
    SELECT
        (AVG(avg_commute * avg_rent) - AVG(avg_commute) * AVG(avg_rent)) / VAR_POP(avg_commute) AS slope,
        AVG(avg_rent) - ((AVG(avg_commute * avg_rent) - AVG(avg_commute) * AVG(avg_rent)) / VAR_POP(avg_commute)) * AVG(avg_commute) AS intercept
    FROM district_stats
)
SELECT
    d.district AS 자치구,
    ROUND(d.avg_commute, 1) AS 평균통근시간_분,
    ROUND(d.avg_rent, 1) AS 실제평균월세_만원,
    ROUND(r.intercept + r.slope * d.avg_commute, 1) AS 예측월세_만원,
    ROUND(d.avg_rent - (r.intercept + r.slope * d.avg_commute), 1) AS 차이_만원
FROM district_stats d
CROSS JOIN city_regression r
ORDER BY 차이_만원 DESC;
