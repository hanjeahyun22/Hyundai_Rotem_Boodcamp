# 다층 신경망 구성 : PyTorch 사용
# PyTorch는 Keras의 model.compile(), model.fit() 같은 고수준 학습 API 대신
# 학습 루프를 직접 작성하는 방식이 일반적이다.
#
# 실습 : 논리회로 OR 게이트 처리를 위한 이진 분류 모델 작성

# OMP 충돌이 발생하는 환경이라면 필요할 수 있음
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# 1) 데이터 수집 및 가공
# OR 게이트 입력 데이터
x = np.array([[0, 0],[0, 1],[1, 0],[1, 1]], dtype=np.float32)
# OR 게이트 정답 데이터
y = np.array([[0],[1],[1],[1]], dtype=np.float32)

# NumPy 배열을 PyTorch Tensor로 변환
x_train = torch.tensor(x)
y_train = torch.tensor(y)

# 2) 모델 네트워크 설정
# 입력 특성 2개를 받아 출력 1개를 만드는 단순 신경망
# Keras의 Dense(units=1) + sigmoid 구조와 비슷함
# 수식으로 보면 y = sigmoid(w1*x1 + w2*x2 + b)
class ORModel(nn.Module):
    def __init__(self):
        super().__init__()

        # 입력 2개 → 출력 1개. Keras의 Dense(units=1)과 비슷한 역할
        self.linear = nn.Linear(2, 1)

        # 이진 분류 확률값 출력을 위한 sigmoid 함수
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 순전파 forward
        x = self.linear(x)
        x = self.sigmoid(x)
        return x

model = ORModel()
print('model:', model) # ORModel((linear): Linear(in_features=2, out_features=1, bias=True)(sigmoid): Sigmoid())

# 3) 모델 학습 과정 설정
# Keras의 compile()에 해당하는 부분을 PyTorch에서는 직접 지정한다.
# loss function:BCELoss는 이진 분류에서 사용하는 손실 함수
#   Keras의 binary_crossentropy와 비슷함
# optimizer:모델의 파라미터를 업데이트하는 알고리즘. 여기서는 Adam 사용
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.1)

# 다른 optimizer 예시
# optimizer = optim.SGD(model.parameters(), lr=0.1)
# optimizer = optim.RMSprop(model.parameters(), lr=0.1)

# 4) 모델 학습 : Keras의 model.fit()에 해당하는 부분
# PyTorch에서는 보통 아래 과정을 직접 작성한다.
# 순전파 → 손실 계산 → 기울기 초기화 → 역전파 → 가중치 업데이트
epochs = 30

for epoch in range(epochs):
    # 1. 순전파 : 입력 데이터를 모델에 넣어 예측값 계산
    pred = model(x_train)

    # 2. 손실 계산 : 예측값과 실제값의 차이 계산
    loss = criterion(pred, y_train)

    # 3. 이전 기울기 초기화
    # PyTorch는 기울기가 누적되므로 매 학습마다 초기화 필요
    optimizer.zero_grad()

    # 4. 역전파 : 손실값을 기준으로 각 파라미터의 기울기 계산
    loss.backward()

    # 5. 가중치 업데이트 : optimizer가 계산된 기울기를 이용해 파라미터 수정
    optimizer.step()

    # 정확도 계산
    with torch.no_grad():
        pred_label = (pred > 0.5).float()
        accuracy = (pred_label == y_train).float().mean()

    print(f"Epoch {epoch + 1:02d}/{epochs} - loss: {loss.item():.4f} - accuracy: {accuracy.item():.4f}")


# 5) 모델 평가 : Keras의 model.evaluate()에 해당
# PyTorch에서는 평가 코드도 직접 작성한다.

model.eval()  # 평가 모드로 전환
# Dropout, BatchNorm 같은 계층이 있을 때 학습/평가 동작이 달라지므로 사용
# 현재 모델에는 큰 영향은 없지만 습관적으로 사용하면 좋음

with torch.no_grad():
    # 평가나 예측 시에는 기울기 계산이 필요 없으므로 no_grad() 사용
    proba = model(x_train)
    loss = criterion(proba, y_train)

    pred = (proba > 0.5).float()
    accuracy = (pred == y_train).float().mean()

print('loss : ', loss.item())
print('accuracy : ', accuracy.item())

# 6) 학습 결과 확인
with torch.no_grad():
    proba = model(x_train)
    pred = (proba > 0.5).int()

print('예측 확률 : ', proba)
print('예측 값 : ', pred.view(-1).numpy())
print('실제 값 : ', y_train.view(-1).numpy().astype('int32'))

# 7) 학습된 모델 저장
# Keras: model.save('tf4model.keras')
# PyTorch: 보통 모델의 파라미터만 state_dict 형태로 저장한다.
torch.save(model.state_dict(), 'torch_or_model.pth')

# 8) 모델 읽기 : 저장된 파라미터를 같은 구조의 모델에 다시 불러온다.
mymodel = ORModel()
mymodel.load_state_dict(torch.load('torch_or_model.pth'))
mymodel.eval()

with torch.no_grad():
    new_proba = mymodel(x_train)
    new_pred = (new_proba > 0.5).int()

print('저장 후 다시 읽은 모델의 예측 값 : ', new_pred.view(-1).numpy())

# 역전파 Backpropagation 설명
# epochs가 2 이상일 때만 역전파가 적용되는 것은 아니다.
# 학습을 1 epoch만 수행해도 아래 과정에서 역전파는 적용된다.
# 순전파 → 손실 계산 → 역전파 → 가중치 업데이트
#
# PyTorch 학습 과정:
# 1. pred = model(x_train)
#    - 순전파 : 입력 데이터를 모델에 넣어 예측값을 계산
# 2. loss = criterion(pred, y_train)
#    - 손실 계산 : 예측값과 정답의 차이를 계산
# 3. optimizer.zero_grad()
#    - 이전 기울기 초기화 : PyTorch는 gradient가 누적되므로 매번 초기화 필요
# 4. loss.backward()
#    - 역전파 : 손실값을 기준으로 각 가중치가 오차에 얼마나 영향을 주었는지 계산
# 5. optimizer.step()
#    - 가중치 업데이트 : optimizer가 계산된 기울기를 이용해 모델 파라미터를 수정
#
# 한마디로 역전파는 손실값을 기준으로 각 가중치의 책임 정도를 계산하고,
# optimizer는 그 결과를 이용해 모델의 가중치를 조금씩 수정한다.
