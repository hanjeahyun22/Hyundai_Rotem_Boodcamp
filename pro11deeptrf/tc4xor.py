# 실습 : XOR 게이트 처리를 위한 이진 분류 모델 작성
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# 1) 데이터 수집 및 가공
x = np.array([[0, 0],[0, 1],[1, 0],[1, 1]], dtype=np.float32)
y = np.array([[0],[1],[1],[0]], dtype=np.float32)

# NumPy 배열을 PyTorch Tensor로 변환
x_train = torch.tensor(x)
y_train = torch.tensor(y)

# 2) 모델 네트워크 설정
# 구조:
# 입력층: 입력 특성 2개
# 은닉층1: Linear(2 -> 5) + ReLU
# 은닉층2: Linear(5 -> 5) + ReLU
# 출력층: Linear(5 -> 1) + Sigmoid
# XOR 문제는 단순 선형 모델로는 해결하기 어렵기 때문에
# 은닉층을 추가해 비선형 패턴을 학습하도록 구성한다.
class XORModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(2, 5),   # 입력 2개 -> 은닉 노드 5개
            nn.ReLU(),         # 활성화 함수 ReLU

            nn.Linear(5, 5),   # 은닉 노드 5개 -> 은닉 노드 5개
            nn.ReLU(),         # 활성화 함수 ReLU

            nn.Linear(5, 1),   # 은닉 노드 5개 -> 출력 1개
            nn.Sigmoid()       # 이진 분류 확률값 출력을 위한 sigmoid
        )

    def forward(self, x):
        return self.net(x)

model = XORModel()
print(model)

# 3) 모델 학습 과정 설정
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 4) 모델 학습
epochs = 200
loss_history = []
accuracy_history = []

for epoch in range(epochs):
    model.train()  # 학습 모드
    proba = model(x_train)
    loss = criterion(proba, y_train)
    # PyTorch는 gradient가 누적되므로 매 epoch마다 초기화 필요
    optimizer.zero_grad()
    loss.backward()

    optimizer.step()  # 가중치 업데이트

    with torch.no_grad():
        pred = (proba > 0.5).float()
        accuracy = (pred == y_train).float().mean()

    loss_history.append(loss.item())
    accuracy_history.append(accuracy.item())

    # epoch별 결과 출력
    print(f"Epoch {epoch + 1:03d}/{epochs} - loss: {loss.item():.4f} - accuracy: {accuracy.item():.4f}")

model.eval()  # 5) 모델 평가

with torch.no_grad():
    proba = model(x_train)
    loss = criterion(proba, y_train)

    pred = (proba > 0.5).float()
    accuracy = (pred == y_train).float().mean()

print('loss_metrics : ', [loss.item(), accuracy.item()])


# 6) 예측 결과 확인
with torch.no_grad():
    proba = model(x_train)
    pred = (proba > 0.5).int()

# 차원을 낮추려면 view(-1), reshape(-1), 또는 squeeze()를 사용
print('예측 확률 : ', proba.view(-1))
print('pred : ', pred.view(-1))

# 학습 과정 시각화 : 직접 리스트에 저장해서 사용한다.
plt.plot(loss_history, label='loss')
plt.plot(accuracy_history, label='accuracy')
plt.xlabel('epochs')
plt.ylabel('loss / accuracy')
plt.legend(loc='best')
plt.show()