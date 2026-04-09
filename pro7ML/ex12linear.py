# LinearRegression 클래스 사용 : 평가 score 정리
"""
LinearRegression 모델의 성능 평가 지표:
1. R2 Score (결정계수): 모델이 데이터의 분산을 얼마나 설명하는지 나타냄 (1에 가까울수록 좋음)
2. MSE (평균제곱오차): 실제값과 예측값 차이의 제곱 평균 (작을수록 좋음)
3. Explained Variance Score (설명 분산 점수): 모델이 타겟 변수의 변동성을 얼마나 잘 잡아내는지 측정
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression  # summary 지원 안함
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler  # 정규화 클래스

# 데이터 생성
sample_size = 100
np.random.seed(1)

x = np.random.normal(0,10,sample_size)
y = np.random.normal(0,10,sample_size) + x * 30
print(x[:5])
print(y[:5])
print('상관계수 : ', np.corrcoef(x,y)[0,1])

print('-' * 40)
# MinMaxScaler: 데이터를 0과 1 사이의 범위로 스케일링하는 함수
# 이상치에 민감할 수 있으나 데이터의 상대적 크기를 유지하며 정규화함
scaler = MinMaxScaler()

# fit_transform(): 데이터의 통계량(최소/최대값)을 학습함과 동시에 변환을 수행하는 함수
# LinearRegression은 2차원 배열 형태의 독립변수를 요구하므로 reshape(-1, 1) 적용
x_scaled = scaler.fit_transform(x.reshape(-1,1))
print(x[:5]) # [ 16.24345364  -6.11756414  -5.28171752 -10.72968622   8.65407629]
print(x_scaled[:5])
# [[0.87492405]
#  [0.37658554]
#  [0.39521325]
#  [0.27379961]
#  [0.70578689]]

# 시각화
# plt.scatter(x,y, c='r')
# plt.scatter(x_scaled,y)
# plt.show()

model = LinearRegression().fit(x_scaled,y)
print('model : ', model)
print('회귀계수(slope) : ', model.coef_)  # [1350.4161554]
print('절편(bias) : ', model.intercept_)  # -691.1877661754081
print('결정계수(R^2) : ', model.score(x_scaled,y))  # 0.9987875127274646

y_pred = model.predict(x_scaled) 
print('예측값 : ', y_pred[:5]) #  [ 490.32381062 -182.64057041 -157.48540955 -321.44435455  261.91825779]
print('실제값 : ', y[:5])      # [ 482.83232345 -171.28184705 -154.41660926 -315.95480141  248.67317034]

print('-' * 40)
# 모델 성늘 확인 함수 작성
def myRegScoreFunc(y_true, y_pred):
    # 결정계수 : 실제 관측값의 분산대비 예측값의 분산을 계산하여 데이터 예측의 정확도 성능 측정 지표
    print(f"r2_score(결정계수) : {r2_score(y_true, y_pred)}") #  0.9987875127274646

    # 모델이 데이터의 분산을 얼마나 잘 설명하는지 나타내는 지표 (오차분산이 작으면 점수가 높아짐)
    print(f"explained_variance_score(설명 분산 점수) : {explained_variance_score(y_true, y_pred)}") # 0.9987875127274646

    # 참고: r2_score와 explained_variance_score가 같은 이유
    # 잔차(오차)의 평균이 0이면 두 값은 일치한다. 
    # OLS(최소제곱법) 방식의 선형회귀 모델은 수학적으로 잔차의 평균을 0으로 만들기 때문에 보통 같은 값이 나온다.

    # 오차를 제곱해 평균 구함(오차가 커질 수록 손실함수값이 빠르게 증가함. 값이 작으면 모델 성능이 우수)
    print(f"mean_squared_error(MSE, 평균제곱오차) : {mean_squared_error(y_true, y_pred)}")  # 86.14795101998747
    imsi = mean_squared_error(y_true, y_pred)  # RMSE로 변환해서 확인
    print(f"root mean_squared_error(RMSE, 평균제곱오차의 제곱근) : {np.sqrt(imsi)}")  # 9.28(평균적으로 약 +-9 오차가 있음)

myRegScoreFunc(y, y_pred)  # 실제값, 예측값

print()
print('분산이 크게 다른 x, y 값을 사용')
x2 = np.random.normal(0,1,sample_size)
y2 = np.random.normal(0,100,sample_size) + x2 * 30
print(x2[:5])
print(y2[:5])
print('상관계수 : ', np.corrcoef(x2,y2)[0,1]) 

x_scaled2 = scaler.fit_transform(x2.reshape(-1,1))

model2 = LinearRegression().fit(x_scaled2,y2)
print('model : ', model2)
print('회귀계수(slope) : ', model2.coef_)  
print('절편(bias) : ', model2.intercept_)
print('결정계수(R^2) : ', model2.score(x_scaled2,y2))

