# 단순선형회귀 모델 작성
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# 1. 데이터 준비
# feature, label을 2차원 형태로 입력하기 위함
# PyTorch의 Linear 계층은 입력 shape을 보통 (데이터개수, feature개수) 형태로 받습니다.
xdata = np.array([1, 2, 3, 4, 5], dtype='float32').reshape(-1, 1)
ydata = np.array([1.2, 2.0, 3.0, 3.5, 5.5], dtype='float32').reshape(-1, 1)

print('상관 계수 : ')
print(np.corrcoef(xdata.ravel(), ydata.ravel()))  # 약 0.97494708

# NumPy 배열을 PyTorch Tensor로 변환
x_tensor = torch.tensor(xdata, dtype=torch.float32)
y_tensor = torch.tensor(ydata, dtype=torch.float32)

# 2. PyTorch 모델 정의
# Keras Sequential 모델:
# Input(1) -> Dense(5, relu) -> Dense(1, linear)
# PyTorch에서는 nn.Module을 상속받아 모델 클래스를 정의하거나,
# nn.Sequential을 사용해서 간단히 모델을 만들 수 있다.

model = nn.Sequential(
    nn.Linear(1, 5),   # 입력 feature 1개 -> 은닉 노드 5개
    nn.ReLU(),         # activation='relu'
    nn.Linear(5, 1)    # 은닉 노드 5개 -> 출력 1개
    # PyTorch에서는 마지막에 별도 activation을 넣지 않으면 linear 출력임.
)
print(model)

# 3. 손실 함수와 옵티마이저를 직접 정의.
criterion = nn.MSELoss()   # 평균제곱오차, mean squared error
optimizer = optim.SGD(model.parameters(), lr=0.01)  # 경사하강법 SGD

# 4. 모델 학습
# Keras의 model.fit()과 달리, PyTorch는 학습 반복문을 직접 작성.
# 학습 순서:
# 1. 예측값 계산 -> 2. 손실값 계산 -> 3. 기존 gradient 초기화 ->
# 4. 역전파로 gradient 계산 -> 5. optimizer로 W, b 갱신
epochs = 100
batch_size = 1

for epoch in range(epochs):
    # shuffle=True 효과를 주기 위해 매 epoch마다 데이터 인덱스를 섞음.
    indices = torch.randperm(len(x_tensor))

    total_loss = 0

    for idx in indices:
        # batch_size=1이므로 데이터 1개씩 꺼냄.
        # Linear 계층 입력은 2차원 형태가 필요하므로 unsqueeze(0) 사용
        x_batch = x_tensor[idx].unsqueeze(0)
        y_batch = y_tensor[idx].unsqueeze(0)

        pred = model(x_batch)  # 1. 예측값 계산
        loss = criterion(pred, y_batch)  # 2. 손실값 계산
        optimizer.zero_grad()  # 3. 이전 gradient 초기화
        loss.backward()   # 4. 역전파
        optimizer.step()  # 5. 파라미터 갱신

        total_loss += loss.item()

    # verbose=1처럼 학습 과정을 출력
    print(f'Epoch [{epoch + 1}/{epochs}], loss: {total_loss / len(x_tensor):.6f}')

# 5. 모델 평가
# 평가 또는 예측 시에는 gradient 계산이 필요 없으므로 torch.no_grad() 사용
with torch.no_grad():
    pred_tensor = model(x_tensor)
    loss_eval = criterion(pred_tensor, y_tensor)

print('loss_eval : ', loss_eval.item())

# 6. 예측 결과 확인
# PyTorch Tensor를 NumPy 배열로 변환할 때는 .detach().numpy() 사용
pred = pred_tensor.detach().numpy()
print('pred : ', pred.ravel())
print('real : ', ydata.ravel())

# 7. 결정계수 R2 계산
print('결정계수(R2, 설명력)')
print('설명력 : ', r2_score(ydata, pred))

# 8. 시각화
plt.scatter(xdata, ydata, color='r', marker='o', label='real')
plt.plot(xdata, pred, 'b--', label='pred')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

# 9. 새로운 값으로 예측
new_x = np.array([1.5, 5.7, -3.0], dtype='float32').reshape(-1, 1)
new_x_tensor = torch.tensor(new_x, dtype=torch.float32)

with torch.no_grad():
    new_pred_tensor = model(new_x_tensor)

new_pred = new_pred_tensor.detach().numpy()
print('새값 예측 결과 : ', new_pred.ravel())