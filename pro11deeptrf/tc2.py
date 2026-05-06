# 연산자와 기초 함수 - PyTorch 버전
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import numpy as np

x = torch.tensor(7)
y = torch.tensor(3)

# PyTorch는 기본적으로 Eager Execution 방식이므로
# TensorFlow의 tf.cond()처럼 별도 조건 함수를 쓰기보다 일반 Python if문을 사용
if x > y:
    result1 = torch.add(x, y)
else:
    result1 = torch.subtract(x, y)

print(result1)  # tensor(10)


# 여러 조건 처리
# PyTorch에서는 tf.case()에 해당하는 함수를 일반적으로 사용하지 않고
# Python의 if ~ elif ~ else 문을 사용
if x < y:
    result2 = torch.tensor(1)
else:
    result2 = torch.multiply(torch.tensor(2), torch.tensor(3))

print(result2)  # tensor(6)

print('관계 연산 ---')
print(torch.eq(torch.tensor(1), torch.tensor(2))) # tensor(False)
print(torch.ne(torch.tensor(1), torch.tensor(2))) # tensor(True)
print(torch.lt(torch.tensor(1), torch.tensor(2))) # tensor(True)
print(torch.gt(torch.tensor(1), torch.tensor(2))) # tensor(False)
print(torch.ge(torch.tensor(1), torch.tensor(2))) # tensor(False)

print('논리 연산 ---')
print(torch.logical_and(torch.tensor(True), torch.tensor(False))) # tensor(False)
print(torch.logical_or(torch.tensor(True), torch.tensor(False))) # tensor(True)
print(torch.logical_not(torch.tensor(True))) # tensor(False)

print('유일 값 unique ---')
kbs = torch.tensor([1, 2, 2, 3, 2]) 
val = torch.unique(kbs)  # torch.unique() : 중복을 제거한 유일 값 반환
print('val : ', val)  # tensor([1, 2, 3])
# return_inverse=True를 주면
# 원래 각 원소가 unique 결과의 몇 번째 값에 해당하는지 인덱스를 반환
val, idx = torch.unique(kbs, return_inverse=True)
print('val : ', val)  # tensor([1, 2, 3])
print('idx : ', idx)  # tensor([0, 1, 1, 2, 1])

print('reduce ~ 함수 ---')
ar = torch.tensor([[1., 2.],[3., 4.]])
print(torch.mean(ar).item())   # 2.5, 전체 평균
print(torch.mean(ar, dim=0).numpy())  # [2. 3.], 각 열의 평균
print(torch.mean(ar, dim=1).numpy())  # [1.5 3.5], 각 행의 평균
print(torch.max(ar).item())    # 4.0, 전체 최대값

print('reshape 함수 ---')
t = np.array([[[0, 1, 2],[3, 4, 5],[6, 7, 8],[9, 10, 11]]])
t_tensor = torch.tensor(t)  # NumPy 배열을 PyTorch Tensor로 변환
print(t_tensor.shape)   # torch.Size([1, 4, 3])
print(torch.reshape(t_tensor, shape=(12,)))   # tensor([ 0,  1,  2,  3,  4, ...]), shape=(12,)
print(torch.reshape(t_tensor, shape=(2, 6)))  # shape=(2, 6)
print(torch.reshape(t_tensor, shape=(-1, 6))) # 행 개수 자동 결정, shape=(2, 6)
print(torch.reshape(t_tensor, shape=(2, -1))) # 열 개수 자동 결정, shape=(2, 6)

print('squeeze 함수 : 차원 축소(shape에서 크기가 1인 차원을 제거) ---')
print(torch.squeeze(t_tensor))
# 원본 shape: (1, 4, 3) squeeze 후 shape: (4, 3) 크기가 1인 첫 번째 차원이 제거됨

t2 = np.array([[[0], [3], [6], [9]]])
t2_tensor = torch.tensor(t2)
print(t2_tensor.shape)   # torch.Size([1, 4, 1])
print(torch.squeeze(t2_tensor))  # tensor([0, 3, 6, 9]) shape: (1, 4, 1) -> (4,)

print('unsqueeze 함수 : 차원 확대 ---')
# TensorFlow의 expand_dims()와 같은 역할
# PyTorch에서는 torch.unsqueeze() 또는 Tensor.unsqueeze()를 사용
tarr = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(tarr.shape)  # torch.Size([2, 3]) : 2행 3열, 2차원 Tensor
sbs = torch.unsqueeze(tarr, 0)
# dim=0 위치에 새 차원 추가  shape: (2, 3) -> (1, 2, 3)
print(sbs.numpy())    # [[[1 2 3] [4 5 6]]]

sbs = torch.unsqueeze(tarr, 1) 
# dim=1 위치에 새 차원 추가    shape: (2, 3) -> (2, 1, 3)
print(sbs.numpy()) # [[[1 2 3]] [[4 5 6]]]

sbs = torch.unsqueeze(tarr, 2)
# dim=2 위치에 새 차원 추가    shape: (2, 3) -> (2, 3, 1)
print(sbs.numpy()) # [[[1][2][3]] [[4][5][6]]]

sbs = torch.unsqueeze(tarr, -1)
# dim=-1은 마지막 위치에 새 차원 추가
# 현재 2차원 Tensor에서는 dim=2와 같은 결과   shape: (2, 3) -> (2, 3, 1)
print(sbs.numpy())  # [[[1][2][3]] [[4][5][6]]]
# 예: 이미지 처리에서 (height, width) 형태의 흑백 이미지를
# (height, width, 1)처럼 채널 차원을 추가할 때 사용 가능

print('type 변환 함수 : 자료형 변환 ---')
num = torch.tensor([1, 2, 3])  # 기본 정수 Tensor, 보통 int64
num2 = num.to(torch.float32)   # 또는 num.float() 사용 가능
print(num2, num2.dtype)  # tensor([1., 2., 3.]) torch.float32