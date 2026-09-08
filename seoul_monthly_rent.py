import pandas as pd

# -------------------------------------------------------------
# 1. 파일 불러오기 (2025, 2026 월세 파일)
# -------------------------------------------------------------
file_2025 = "4. 2025 서울시 월세 면적.csv"
file_2026 = "4. 2026 서울시 월세 면적.csv"

# 공공데이터 한글 인코딩 처리
try:
    df_2025 = pd.read_csv(file_2025, encoding='cp949')
    df_2026 = pd.read_csv(file_2026, encoding='cp949')
except UnicodeDecodeError:
    df_2025 = pd.read_csv(file_2025, encoding='utf-8')
    df_2026 = pd.read_csv(file_2026, encoding='utf-8')

# 두 연도 데이터 통합
df = pd.concat([df_2025, df_2026], ignore_index=True)

# 컬럼명 앞뒤 공백 제거
df.columns = df.columns.str.strip()

print(f"통합 전 전체 데이터 건수: {len(df):,}건")

# -------------------------------------------------------------
# 2. 실제 데이터 컬럼명 설정 (이미지 기반)
# -------------------------------------------------------------
col_gu = '자치구명'        # 자치구 컬럼
col_area = '임대면적'      # 임대면적 컬럼
col_building = '건물용도'  # 건물용도 (아파트, 오피스텔, 연립다세대, 단독다가구)

# -------------------------------------------------------------
# 3. 이미지 조건 기반 정제 (결측치 & 130m² 초과 삭제)
# -------------------------------------------------------------
df_clean = df.copy()

# [조건 1] 자치구명 결측치(NaN) 제거 (2025년 2건)
df_clean = df_clean.dropna(subset=[col_gu])

# [조건 2] 임대면적 130m² 초과 삭제 (2025년 11,383건 + 2026년 4,056건)
df_clean = df_clean[df_clean[col_area] <= 130]

print(f"정제 후 최종 남아있는 데이터 건수: {len(df_clean):,}건")

# -------------------------------------------------------------
# 4. 구·건물용도별 데이터 집계 (평균 면적 및 거래건수)
# -------------------------------------------------------------
summary = df_clean.groupby([col_gu, col_building]).agg(
    평균_임대면적_m2=(col_area, 'mean'),
    월세_거래건수=(col_area, 'count')
).reset_index().round(2)

# -------------------------------------------------------------
# 5. 최종 정제 결과 파일 저장 (cleaned_ 접두사)
# -------------------------------------------------------------
output_file = "cleaned_seoul_monthly_rent_area_summary.csv"
summary.to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n전처리 완벽 성공! '{output_file}' 파일로 저장되었습니다.")
print(summary.head(10))