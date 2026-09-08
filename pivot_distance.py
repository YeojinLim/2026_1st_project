# -*- coding: utf-8 -*-
"""
주요역소요시간.csv 를 long -> wide 형태로 pivot
  - 원본: 구 1개당 3줄 (강남역/광화문역/여의도역 각각 한 행씩)
  - 결과: 구 1개당 1줄, 도착역별 소요시간이 각각 컬럼으로 펼쳐짐
"""

import pandas as pd

RAW_PATH = r"C:\Users\user\Desktop\csv 파일\6. 주요역소요시간.csv"
OUT_DIR = r"C:\Users\user\Desktop\csv 파일\\"

df = pd.read_csv(RAW_PATH, encoding="cp949")
print(f"[원본] {len(df)}행 (long 형태)")

# 소요시간 wide 변환
time_wide = df.pivot(index=["구", "대표역"], columns="도착역",
                      values="소요시간(카카오맵, 분 기준)")
time_wide.columns = [f"{c}_소요시간(분)" for c in time_wide.columns]

# 환승횟수도 같은 방식으로 wide 변환 (참고용으로 함께 보관)
transfer_wide = df.pivot(index=["구", "대표역"], columns="도착역",
                          values="환승 횟수(최저 환승)")
transfer_wide.columns = [f"{c}_환승횟수" for c in transfer_wide.columns]

result = pd.concat([time_wide, transfer_wide], axis=1).reset_index()

print(f"\n[변환 결과] {len(result)}행 (wide 형태, 구 1개당 1행)")
print(result.head())

result.to_csv(OUT_DIR + "cleaned_distance_wide.csv", index=False, encoding="utf-8-sig")
print("\n[저장 완료] cleaned_distance_wide.csv")
