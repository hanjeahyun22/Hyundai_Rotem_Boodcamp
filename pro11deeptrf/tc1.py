# Tensor → NumPy 차이 → 형변환 → Tensor 값 변경 → in-place 연산 → 난수 흐름

# OMP: Error:libiomp5md.dll이라는 OpenMP 런타임 DLL이 중복 로딩되어 발생하는 경우
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"   # 임시 우회 방법
# tf와 PyTorch 예제는 가능하면 분리하는 게 좋다. (가상 환경 분리)

import torch
import numpy as np

print(torch.__version__)   # 2.11.0+cpu
# PyTorch는 기본적으로 Eager Execution 방식으로 동작

print('GPU 사용 가능 여부 : ', torch.cuda.is_available())  # False
print('GPU 장치 정보 : ', torch.cuda.get_device_name(0) if torch.cuda.is_available() else []) # []

print('\nTensor : PyTorch에서 데이터를 담는 기본 자료구조 (숫자 데이터 저장용 다차원 배열)')
# ndarray와 유사하지만 PyTorch 연산에 사용되도록 만들어진 객체
# PyTorch의 Tensor는 딥러닝 연산, GPU 연산, 자동 미분 등에 사용됨
print(12, type(12))  # 12 <class 'int'> 파이썬 상수로 파이썬이 직접 계산
print(torch.tensor(12)) # tensor(12)   0d 텐서 (scalar)
print(torch.tensor([12]))  # tensor([12])    1d 텐서 (vector)
print(torch.tensor([[12]]))  # tensor([[12]])   2d 텐서 (matrix)
print(torch.tensor([[12, 1]]))  # tensor([[12,  1]])

# 2, 텐서의 차원 수 확인
print(torch.tensor([[12, 1]]).dim())  # 2
print(torch.tensor([[12, 1]]).ndim)   # 2, dim()과 같은 의미
print(torch.tensor(12))  # tensor(12)  일반 print()로 Tensor 값을 확인함

print('\nTensor 속성 확인 ---------')
t = torch.tensor([[1, 2, 3],[4, 5, 6]], dtype=torch.float32)
print('shape : ', t.shape)   # torch.Size([2, 3])
print('dtype : ', t.dtype)   # torch.int64
print('dim : ', t.dim())     # 2

print()
imsi = np.array([1, 2])  
# NumPy 배열: 일반 수치 연산에 사용, CPU 연산이 기본, 자동 미분 불가, 값 변경 가능
print(imsi, type(imsi))   # [1 2] <class 'numpy.ndarray'>
imsi[0] = 10  # NumPy 배열은 값 변경 가능
print(imsi)   # [10  2]

# PyTorch Tensor: 딥러닝 연산과 GPU 연산에 사용할 수 있는 기본 자료구조
a = torch.tensor([1, 2])  
print(type(a))  # <class 'torch.Tensor'>

# tf의 tf.constant는 값 변경 불가하나, torch.tensor는 값 변경이 가능함
a[0] = 10
print(a) # tensor([10,  2])

# 다시 원래 예제를 위해 a 재선언
a = torch.tensor([1, 2])
b = torch.tensor([3, 4])
c = a + b  # 텐서 요소값 더하기
print(c)   # tensor([4, 6])
d = torch.tensor([3])
e = c + d
print(e)   # tensor([7, 9]) Broadcast 연산

print('\n파이썬, NumPy, PyTorch 형변환 가능')
print(7)   # 7
print(torch.tensor(7))  # tensor(7)
print(torch.tensor(7).item())   # 7, 스칼라 Tensor를 파이썬 숫자로 변환
print(torch.tensor([1, 2]).numpy())  # Tensor를 NumPy 배열로 변환

arr = np.array([1, 2])  # ndarray type
torch_arr = torch.tensor(arr)  # NumPy 배열을 PyTorch Tensor로 변환
print(torch_arr)  # tensor([1, 2])

# 사칙 연산 가능
# torch.add(), torch.subtract(), torch.multiply(), torch.divide() 가능
torch_result = torch.add(torch_arr, 5)
print(torch_result)  # tensor([6, 7])

# PyTorch Tensor를 NumPy 배열로 변환 후 NumPy 연산
np_result = np.add(torch_result.numpy(), 2)
print(np_result)  # [8 9]

print('\nPyTorch Tensor 선언 후 사용하기 ---------')
# tf.Variable() 사용안함
# PyTorch에서는 torch.tensor() 자체가 값을 변경할 수 있음
v1 = torch.tensor(1.0)  # 하나의 숫자 값을 가진 PyTorch Tensor 생성
print('변경 전 v1 : ', v1)  # tensor(1.)
v1.fill_(100)           # 기존 Tensor의 모든 값을 100으로 변경
print('변경 후 v1 : ', v1)  # tensor(100.)
    # PyTorch Tensor는 기본적으로 변경 가능한 객체이며,
    # 값을 직접 바꾸는 메서드는 보통 이름 끝에 _가 붙는다.
    # 예: fill_(), copy_(), add_(), sub_(), mul_(), div_()
    # 참고로 PyTorch에서 일반 Tensor는 값 변경은 가능하지만, 자동 미분 대상은 아님
    # 학습 가능한 가중치로 사용하려면 requires_grad=True를 지정하거나
    # nn.Parameter로 만들어 모델의 학습 파라미터로 등록해야 함.
    # 단, requires_grad=True는 보통 실수형 Tensor에 사용함
    # 예 : w = torch.tensor(2.0, requires_grad=True)

print('\n간단한 선형식 y = wx + b ---------')
x = torch.tensor(3.0)
w = torch.tensor(2.0)
b = torch.tensor(1.0)
y = w * x + b
print('x : ', x)
print('w : ', w)
print('b : ', b)
print('y = wx + b : ', y)   # tensor(7.)

print()
# TensorFlow: v1.assign(123)이고, 
# PyTorch에서는 copy_(), fill_(), 인덱싱 대입, in-place 연산 등을 사용
v1 = torch.tensor(1.0)
v1.copy_(torch.tensor(123.0))  # 기존 Tensor에 새 값 복사
print('v1 : ', v1)  # tensor(123.)
v2 = torch.ones((2, ))   # 값이 1로 채워진 크기 2의 Tensor 생성
v2.copy_(torch.tensor([30.0, 40.0]))
print('v2 : ', v2)  # tensor([30., 40.])

print()
aa = torch.zeros((2, 1))   # 2행 1열에 모두 0을 가진 Tensor 생성
print('aa : ', aa)  # tensor([[0.],[0.]])
aa.copy_(torch.ones((2, 1)))  # TensorFlow의 assign()과 비슷한 역할
print('aa : ', aa)  # tensor([[1.],[1.]])

aa.add_(torch.tensor([[2.0], [3.0]]))  # 더하기 후 치환
# TensorFlow의 assign_add()와 비슷함
# PyTorch에서 메서드 뒤에 _가 붙으면 원본 Tensor를 직접 변경하는 in-place 연산
print('aa : ', aa)  # tensor([[3.], [4.]])

aa.sub_(torch.tensor([[2.0], [3.0]]))  # 빼기 후 치환. Tf의 assign_sub()와 비슷
print('aa : ', aa)  # tensor([[1.], [1.]])
aa.mul_(torch.tensor([[2.0], [3.0]]))  # 곱하기 후 치환
print('aa : ', aa)  # tensor([[2.], [3.]])
aa.div_(torch.tensor([[2.0], [3.0]]))  # 나누기 후 치환
print('aa : ', aa)  # tensor([[1.], [1.]])

print('\n난수 처리')
print(torch.rand(1))  # tensor([0.1088]) 값은 동적임

# 균등분포: 0 이상 1 미만 사이에서 난수 생성
# 크기가 2인 빈 Tensor를 만든 뒤, 그 안을 0 이상 1 미만의 균등분포 난수로 채움
print(torch.empty(2).uniform_(0, 1))  # tensor([0.9129, 0.3498])

print(torch.randn(3))   # 정규분포: 평균 0, 표준편차 1을 기준으로 난수 생성
# tensor([-1.3246,  1.7092,  1.1448])

print(torch.normal(mean=0.0, std=1.0, size=(3, 2))) # 3행 2열 형태의 정규분포 난수 생성
# tensor([[-0.9844, -0.7033], [ 1.3883,  0.7606], [-1.2574,  1.5060]])

print('\n재현 가능한 난수 처리 ---------')
torch.manual_seed(42)  # seed를 고정하면 같은 난수 결과를 재현할 수 있음
print(torch.rand(3))  # tensor([0.8823, 0.9150, 0.3829])


# 핵심 차이 --------------------
# TensorFlow
#   - tf.constant() : 값 변경 불가
#   - tf.Variable() : 값 변경 가능
#   - assign(), assign_add(), assign_sub() 사용
# PyTorch
#   - torch.tensor() : 기본 Tensor이며 값 변경 가능
#   - copy_(), add_(), sub_(), mul_(), div_() 같은 in-place 연산 사용
#   - 메서드 이름 뒤의 _는 원본 Tensor를 직접 변경한다는 의미

# 특히 이 부분 이해하자.
# aa.add_(값)   # 원본 aa가 직접 변경됨
# aa + 값       # 새 Tensor가 만들어짐, 원본 aa는 그대로

# PyTorch는 기본적으로 Eager Execution 방식으로 동작한다.
# 즉, 일반 Python 코드처럼 if, for, while을 그대로 사용할 수 있다.
# 기본적으로 tf의 @tf.function / AutoGraph처럼 그래프 변환을 신경 쓸 필요가 없다.

