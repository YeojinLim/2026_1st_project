# -*- coding: utf-8 -*-
"""
2024 서울시 청년 연간총소득평균 -> 참조 테이블(reference table)로 정리
  - 구별 분해 없음 (서울 전체 값 1개 + 연령별/지역구분별 값)
  - RIR(주거비부담지수) 계산 시 공통 분모로 사용할 값을 명확히 저장
"""

import pandas as pd

RAW_PATH = r"C:\Users\user\Desktop\csv 파일\5. 2024 서울시 청년 연간총소득평균.csv"
OUT_DIR = r"C:\Users\user\Desktop\csv 파일\\"

df = pd.read_csv(RAW_PATH, encoding="cp949")

# 실제 데이터는 1번 행부터 시작 (0번 행은 헤더성 텍스트)
df = df.iloc[1:].reset_index(drop=True)
df.columns = ["구분", "세부항목", "연소득_만원"]
df["연소득_만원"] = pd.to_numeric(df["연소득_만원"], errors="coerce")

print(df)

# KPI 계산에 바로 쓸 서울 전체 대표값 (RIR 공통 분모)
seoul_avg = df.loc[df["세부항목"] == "서울", "연소득_만원"].values[0]
print(f"\n[RIR 계산용 서울 청년 개인 연소득 평균] {seoul_avg}만원")
print("-> 자치구별 분해가 없어 이 값을 전 구 공통 분모로 사용함 (보고서에 한계 명시 필요)")

df.to_csv(OUT_DIR + "ref_소득평균_2024.csv", index=False, encoding="utf-8-sig")
print("\n[저장 완료] ref_소득평균_2024.csv")
