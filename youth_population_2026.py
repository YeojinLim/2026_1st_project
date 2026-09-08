import csv

# 원본 CSV 파일
file_name = "2026 서울시 구별 청년 등록인구.csv"

# 처리한 데이터를 저장할 리스트
data = []

with open(file_name, "r", encoding="cp949", newline="") as file:

    reader = csv.reader(file)

    # 첫 번째, 두 번째 행은 헤더이므로 제거
    next(reader)
    next(reader)

    # 실제 데이터 읽기
    for row in reader:

        # '계'만 남기기
        if row[1] != "계":
            continue

        # 전체 합계 제거
        if row[0] == "합계":
            continue

        # 필요한 데이터만 저장
        data.append([
            row[0],  # 자치구
            row[2],  # 20~24세
            row[3],  # 25~29세
            row[4],  # 30~34세
            row[5]   # 35~39세
        ])


# 새 컬럼명
columns = [
    "자치구",
    "20~24세",
    "25~29세",
    "30~34세",
    "35~39세"
]


# 처리한 데이터를 새로운 CSV 파일로 저장
output_file = "2026_서울시_구별_청년등록인구_처리.csv"

with open(output_file, "w", encoding="utf-8-sig", newline="") as file:

    writer = csv.writer(file)

    # 컬럼명 저장
    writer.writerow(columns)

    # 데이터 저장
    writer.writerows(data)


print(f"처리된 CSV 파일이 저장되었습니다: {output_file}")