import pandas as pd
import scipy.stats as stats
import numpy as np
# [two-sample t 검정 : 문제2]  
# 아래와 같은 자료 중에서 남자와 여자를 각각 15명씩 무작위로 비복원 추출하여 혈관 내의 콜레스테롤 양에 차이가 있는지를 검정하시오.
# 수집된 자료 :  
man = [0.9, 2.2, 1.6, 2.8, 4.2, 3.7, 2.6, 2.9, 3.3, 1.2, 3.2, 2.7, 3.8, 4.5, 4, 2.2, 0.8, 0.5, 0.3, 5.3, 5.7, 2.3, 9.8]
woman = [1.4, 2.7, 2.1, 1.8, 3.3, 3.2, 1.6, 1.9, 2.3, 2.5, 2.3, 1.4, 2.6, 3.5, 2.1, 6.6, 7.7, 8.8, 6.6, 6.4]

# 가설 설정
# 귀무 : 성별에 따른 혈관 내의 콜레스테롤 양에 차이가 없다.
# 대립 : 성별에 따른 혈관 내의 콜레스테롤 양에 차이가 있다.

man_ran = np.random.choice(man, 15, replace=False)
woman_ran = np.random.choice(woman, 15, replace=False)

print(f"사전 평균: {np.mean(man_ran):.2f}")  # 사전 평균: 3.03
print(f"사후 평균: {np.mean(woman_ran):.2f}")   # 사후 평균: 3.21
print(f"차이 평균: {np.mean(np.array(man_ran) - np.array(woman_ran)):.2f}")  # 차이 평균: -0.18

# 대응표본 t-검정 수행
t_stat, p_val = stats.ttest_rel(man_ran, woman_ran)

print(f"t-통계량: {t_stat:.4f}")  # t-통계량: -0.2716
print(f"p-value: {p_val:.4f}")    # p-value: 0.7899

# [최종 판정] 유의수준 0.05 기준
# p-value(0.7899) > 0.05 이므로 귀무가설을 채택한다.
# 결론: 성별에 따른 혈관 내의 콜레스테롤 양에 차이가 있다고 할 수 없다. (평균 차이가 무의미함)

print('-'*40)
# [two-sample t 검정 : 문제3]
# DB에 저장된 jikwon 테이블에서 총무부, 영업부 직원의 연봉의 평균에 차이가 존재하는지 검정하시오.
# 연봉이 없는 직원은 해당 부서의 평균연봉으로 채워준다.

import pymysql
import pandas as pd
import scipy.stats as stats
import csv

# 1. 데이터베이스 접속 설정
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123',
    'database': 'test',
    'port': 3306,
    'charset': 'utf8'
}

try:
    # 2. DB 연결 및 데이터 로드
    conn = pymysql.connect(**config)    
    sql = "SELECT busername, jikwonpay FROM jikwon INNER JOIN buser ON buserno = busernum"
    
    df = pd.read_sql(sql, conn)
    df.columns = ['부서', '연봉']

    # 3. 데이터 전처리 (부서별 평균 연봉으로 결측치 채우기)
    # 총무부와 영업부 데이터만 필터링
    df = df[df['부서'].isin(['총무부', '영업부'])]
    
    # 부서별 평균 계산 (결측치 제외한 평균)
    avg_pay = df.groupby('부서')['연봉'].transform('mean')
    df['연봉'] = df['연봉'].fillna(avg_pay)

    # 4. 집단 분리
    chong = df[df['부서'] == '총무부']['연봉']
    young = df[df['부서'] == '영업부']['연봉']

    print(f"총무부 평균 연봉: {chong.mean():.2f}")  # 5414.29
    print(f"영업부 평균 연봉: {young.mean():.2f}")  # 4908.33

    # 5. 가설 설정
    # H0: 총무부와 영업부 직원의 연봉 평균에 차이가 없다.
    # H1: 총무부와 영업부 직원의 연봉 평균에 차이가 있다.

    # 6. 정규성 및 등분산성 확인
    # (표본이 적을 경우 수행하나, 여기서는 독립표본 t-검정 절차에 따름)
    _, p_normal1 = stats.shapiro(chong)
    _, p_normal2 = stats.shapiro(young)
    _, p_equal_var = stats.levene(chong, young)

    # 7. 독립표본 t-검정 수행
    # 등분산성 여부에 따라 equal_var 설정
    is_equal = p_equal_var > 0.05
    t_stat, p_val = stats.ttest_ind(chong, young, equal_var=is_equal)

    print("-" * 40)
    print(f"t-통계량 : {t_stat:.4f}")  # 0.4585
    print(f"p-value : {p_val:.4f}")    # 0.6524
    print("-" * 40)

    # 8. 최종 판정
    # [판정] p >= 0.05 이므로 귀무가설 채택.
    # [결론] 총무부와 영업부의 연봉 평균은 차이가 있다고 볼 수 없습니다.

except Exception as e:
    print(f"처리 중 오류 발생: {e}")
finally:
    if 'conn' in locals():
        conn.close()


# [대응표본 t 검정 : 문제4]
# 어느 학급의 교사는 매년 학기 내 치뤄지는 시험성적의 결과가 실력의 차이없이 비슷하게 유지되고 있다고 말하고 있다. 
# 이 때, 올해의 해당 학급의 중간고사 성적과 기말고사 성적은 다음과 같다. 점수는 학생 번호 순으로 배열되어 있다.
# 수집된 자료 :  
#    중간 : 80, 75, 85, 50, 60, 75, 45, 70, 90, 95, 85, 80
#    기말 : 90, 70, 90, 65, 80, 85, 65, 75, 80, 90, 95, 95
# 그렇다면 이 학급의 학업능력이 변화했다고 이야기 할 수 있는가?

mid = [80, 75, 85, 50, 60, 75, 45, 70, 90, 95, 85, 80]
final = [90, 70, 90, 65, 80, 85, 65, 75, 80, 90, 95, 95]

# 가설 설정
# 귀무(H0): 중간고사와 기말고사 성적의 평균 차이가 없다. (학업능력 변화 없음)
# 대립(H1): 중간고사와 기말고사 성적의 평균 차이가 있다. (학업능력 변화 있음)

print(f"중간고사 평균: {np.mean(mid):.2f}")  # 중간고사 평균: 74.17
print(f"기말고사 평균: {np.mean(final):.2f}")  # 기말고사 평균: 81.67

# 대응표본 t-검정 수행 (동일 학생의 사전/사후 비교)
t_stat, p_val = stats.ttest_rel(mid, final)

print(f"t-통계량: {t_stat:.4f}")  # t-통계량: -2.6281
print(f"p-value: {p_val:.4f}")    # p-value: 0.0235

# [최종 판정] 유의수준 0.05 기준
# p-value(0.0235) < 0.05 이므로 귀무가설을 기각한다.
# 결론: 중간고사와 기말고사 성적의 평균 차이가 유의미하므로 학업능력이 변화했다고 할 수 있다.
