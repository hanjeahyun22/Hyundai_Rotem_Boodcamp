# 다중선형회귀 : 자동차 연비 예측
# 조기종료 EarlyStopping 직접 구현
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score
import copy

# 재현성 설정
torch.manual_seed(123)
np.random.seed(123)

# 데이터 읽기
datas = pd.read_csv(
    "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/auto-mpg.csv",
    na_values='?'
)
print(datas.head(2))
print(datas.info())
del datas['car name']    # 사용하지 않을 컬럼 제거
datas = datas.dropna()   # 결측치 제거
print(datas.isna().sum())

# 일부 컬럼 제거
datas.drop(
    ['cylinders', 'acceleration', 'model year', 'origin'],
    axis='columns', inplace=True
)
print(datas.head(2))

# train / test split
train_dataset = datas.sample(frac=0.7, random_state=123)
print(train_dataset[:2], train_dataset.shape)  # (274, 4)
test_dataset = datas.drop(train_dataset.index)
print(test_dataset[:2], test_dataset.shape)  # (118, 4)

# 표준화 기준 계산 : 공식 : (요소값 - 평균) / 표준편차
train_stat = train_dataset.describe()
train_stat.pop('mpg')
print(train_stat)

train_stat = train_stat.transpose()
print(train_stat)

def stdscale_func(x):
    return (x - train_stat['mean']) / train_stat['std']

# 학습 데이터 표준화
st_train_data = stdscale_func(train_dataset)
st_train_data = st_train_data.drop(['mpg'], axis='columns')
print(st_train_data[:3])

# 테스트 데이터 표준화
st_test_data = stdscale_func(test_dataset)
st_test_data = st_test_data.drop(['mpg'], axis='columns')
print(st_test_data[:3])

# label 분리
train_label = train_dataset.pop('mpg')
print(train_label[:3])
test_label = test_dataset.pop('mpg')
print(test_label[:3])

# PyTorch Tensor 변환
x_data = torch.tensor(st_train_data.values, dtype=torch.float32)
y_data = torch.tensor(train_label.values, dtype=torch.float32).view(-1, 1)

x_test = torch.tensor(st_test_data.values, dtype=torch.float32)
y_test = torch.tensor(test_label.values, dtype=torch.float32).view(-1, 1)


# train / validation split : Keras의 validation_split=0.2와 비슷
dataset_size = len(x_data)
val_size = int(dataset_size * 0.2)
train_size = dataset_size - val_size

# 0부터 dataset_size - 1까지의 숫자를 무작위 순서로 섞은 인덱스 배열 생성.
# 무작위로 섞어서: 3, 0, 7, 1, 9, 4, 2, 8, 5, 6 처럼 만든 것
indices = torch.randperm(dataset_size)

train_indices = indices[:train_size]
val_indices = indices[train_size:]

x_train = x_data[train_indices]
y_train = y_data[train_indices]

x_val = x_data[val_indices]
y_val = y_data[val_indices]

print("train shape :", x_train.shape, y_train.shape)
print("val shape :", x_val.shape, y_val.shape)

# DataLoader 생성
batch_size = 32

train_ds = TensorDataset(x_train, y_train)
train_loader = DataLoader(
    train_ds,
    batch_size=batch_size,
    shuffle=True
)

# PyTorch 모델 정의
class MpgModel(nn.Module):
    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(3, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.net(x)

model = MpgModel()
print(model)

# 손실 함수와 optimizer 정의 : Keras compile()에 해당하는 부분
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# EarlyStopping 설정
EPOCHS = 5000
patience = 5
best_val_loss = float('inf')
best_model_state = None
wait = 0

history = {
    'mean_squared_error': [],
    'mean_absolute_error': [],
    'val_mean_squared_error': [],
    'val_mean_absolute_error': []
}

# 모델 학습
for epoch in range(EPOCHS):
    model.train()  # 학습 모드

    train_losses = []
    train_maes = []

    for batch_x, batch_y in train_loader:
        pred = model(batch_x)   # 예측
        loss = criterion(pred, batch_y)  # 손실 계산
        optimizer.zero_grad()   # 기존 gradient 초기화
        loss.backward()   # 역전파
        optimizer.step()  # 가중치 업데이트

        # batch별 mse, mae 저장
        mse = loss.item()
        mae = torch.mean(torch.abs(pred - batch_y)).item()

        train_losses.append(mse)
        train_maes.append(mae)

    train_mse = np.mean(train_losses)
    train_mae = np.mean(train_maes)

    model.eval()  # 검증 모드

    with torch.no_grad():
        val_pred = model(x_val)
        val_mse = criterion(val_pred, y_val).item()
        val_mae = torch.mean(torch.abs(val_pred - y_val)).item()

    # 학습 기록 저장
    history['mean_squared_error'].append(train_mse)
    history['mean_absolute_error'].append(train_mae)
    history['val_mean_squared_error'].append(val_mse)
    history['val_mean_absolute_error'].append(val_mae)

    print(
        f"Epoch {epoch + 1:4d} "
        f"- mse: {train_mse:.4f} "
        f"- mae: {train_mae:.4f} "
        f"- val_mse: {val_mse:.4f} "
        f"- val_mae: {val_mae:.4f}"
    )

    # EarlyStopping 처리 : monitor='val_loss'와 같은 역할
    # 여기서는 val_mse를 기준으로 조기 종료 판단
    if val_mse < best_val_loss:
        best_val_loss = val_mse

        # restore_best_weights=True와 같은 역할
        best_model_state = copy.deepcopy(model.state_dict())
        wait = 0
    else:
        wait += 1

        if wait >= patience:
            print(f"\nEarlyStopping 발생! epoch {epoch + 1}에서 학습 중단")
            print(f"가장 좋은 val_mse : {best_val_loss:.4f}")

            # 가장 성능이 좋았던 epoch의 가중치 복원
            model.load_state_dict(best_model_state)
            break

# 학습 결과 DataFrame 변환
df = pd.DataFrame(history)
df['epoch'] = range(len(df))
print(df.head(3))
print(df.columns)

# 모델 학습 정보 시각화
def plt_history(df):
    hist = df

    plt.figure(figsize=(8, 12))
    plt.subplot(2, 1, 1)
    plt.xlabel('epoch')
    plt.ylabel('mae [mpg]')
    plt.plot(hist['epoch'], hist['mean_absolute_error'], label='train err')
    plt.plot(hist['epoch'], hist['val_mean_absolute_error'], label='validation err')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.xlabel('epoch')
    plt.ylabel('mse [mpg]')
    plt.plot(hist['epoch'], hist['mean_squared_error'], label='train err')
    plt.plot(hist['epoch'], hist['val_mean_squared_error'], label='validation err')
    plt.legend()
    plt.show()

plt_history(df)

model.eval()  # 모델 평가

with torch.no_grad():
    test_pred = model(x_test)

    loss = criterion(test_pred, y_test).item()
    mse = loss
    mae = torch.mean(torch.abs(test_pred - y_test)).item()

print(f'loss {loss:.3f}')
print(f'mse {mse:.3f}')
print(f'mae {mae:.3f}')

test_pred_np = test_pred.numpy().ravel()
test_label_np = y_test.numpy().ravel()
print('결정 계수 : ', r2_score(test_label_np, test_pred_np))

# 새로운 값으로 예측
new_data = pd.DataFrame({
    'displacement': [300, 400],
    'horsepower': [120, 150],
    'weight': [2000, 4000]
})

new_st_data = stdscale_func(new_data)
new_x = torch.tensor(new_st_data.values, dtype=torch.float32)
model.eval()

with torch.no_grad():
    new_data_pred = model(new_x).numpy().ravel()

print('새 값 예측결과 : ', new_data_pred)