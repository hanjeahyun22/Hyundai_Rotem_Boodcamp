"""
SVM(Support Vector Machine) & PCA(주성분 분석) - 얼굴 이미지 분류 실습
---------------------------------------------------------------------------------------------------
1. 개요 (Overview): 
    - LFW(Labeled Faces in the Wild) 데이터셋을 활용하여 유명 정치인들의 얼굴을 분류함
    - 고차원 이미지 데이터(2914개 특성)를 PCA로 차원 축소하여 학습 효율과 일반화 성능을 극대화함

2. 주요 기법 (Key Techniques):
    - PCA: 이미지의 핵심 특징(Eigenfaces)을 추출하여 데이터의 차원을 획기적으로 줄임
    - Pipeline: 전처리(PCA)와 모델(SVM)을 하나로 결합하여 워크플로우를 자동화함
    - SVM: RBF 커널을 사용하여 축소된 특징 공간에서 비선형 분류를 수행함
---------------------------------------------------------------------------------------------------
"""

from sklearn.datasets import fetch_lfw_people
import koreanize_matplotlib
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.decomposition import PCA 
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import seaborn as sns


# =========================================================================
# [STEP 1] 데이터 로드 및 탐색 (Data Loading & Exploration)
# =========================================================================
print("="*70)
print("[STEP 1] 데이터 로드 및 탐색 (LFW People Dataset)")
print("="*60)

# min_faces_per_person: 최소 60장 이상의 이미지가 있는 인물만 선택
faces = fetch_lfw_people(min_faces_per_person=60, color=False, resize=0.5)

print(f"데이터 크기: {faces.data.shape}")      # (1348, 2914) -> 62x47 픽셀
print(f"타겟 인물: {faces.target_names}")
print(f"이미지 구조: {faces.images.shape}")    # (1348, 62, 47)

# [시각화] 원본 이미지 샘플 확인
"""
fig, ax = plt.subplots(3, 5, figsize=(10, 6))
for i, axi in enumerate(ax.flat):
    axi.imshow(faces.images[i], cmap='bone')
    axi.set(xticks=[], yticks=[], xlabel=faces.target_names[faces.target[i]])
plt.suptitle('원본 이미지 샘플')
plt.show()
"""

# =========================================================================
# [STEP 2] PCA 차원 축소 및 특징 추출 (Feature Extraction)
# =========================================================================
print("\n" + "="*70)
print("[STEP 2] PCA 차원 축소: Eigenfaces 추출")
print("="*60)

"""
[PCA 옵션 설명]
1. n_components: 추출할 주성분의 개수 (차원 축소 목표치)
2. whiten: 각 주성분의 분산을 1로 스케일링하여 SVM 성능 향상에 도움을 줌
3. random_state: 결과 재현성을 위한 난수 시드
"""
n_comp = 100
m_pca = PCA(n_components=n_comp, whiten=True, random_state=0) 
x_low = m_pca.fit_transform(faces.data)
print(f"차원 축소 결과: {faces.data.shape[1]} -> {x_low.shape[1]}")

# [시각화] 주성분(Eigenfaces) 이미지 확인
"""
fig, ax = plt.subplots(2, 5, figsize=(10, 5))
for i, axi in enumerate(ax.flat):
    axi.imshow(m_pca.components_[i].reshape(62, 47), cmap='bone')
    axi.set_title(f'특징 {i+1}')
    axi.axis('off')
plt.suptitle('Eigenfaces (추출된 얼굴 특징 패턴)')
plt.show()
"""

print(f"100개 주성분의 누적 설명력: {np.sum(m_pca.explained_variance_ratio_):.4f}")

# =========================================================================
# [STEP 3] 데이터 분할 및 모델 파이프라인 구축 (Modeling)
# =========================================================================
print("\n" + "="*70)
print("[STEP 3] 데이터 분할 및 PCA + SVM 파이프라인 구축")
print("="*60)

# 1. 데이터 분할 (stratify를 통해 인물별 비율 유지)
x_train, x_test, y_train, y_test = train_test_split(
    faces.data, faces.target, stratify=faces.target, random_state=1
)

"""
[SVC 옵션 설명]
1. kernel='rbf': 비선형 결정 경계를 찾기 위한 방사 기저 함수 커널
2. class_weight='balanced': 데이터 양이 적은 클래스에 가중치를 부여하여 불균형 해소
3. C: 규제 파라미터 (오차 허용 범위 조절)
"""

# 2. 파이프라인 생성 (전처리 PCA와 분류기 SVC를 하나로 결합)
svc_model = SVC(C=1, kernel='rbf', class_weight='balanced', random_state=0)
model_pipe = make_pipeline(m_pca, svc_model)

# 3. 모델 학습
model_pipe.fit(x_train, y_train)
print("PCA + SVM 파이프라인 학습 완료")

# =========================================================================
# [STEP 4] 모델 예측 및 성능 평가 (Evaluation)
# =========================================================================
print("\n" + "="*70)
print("[STEP 4] 모델 성능 평가 및 상세 보고서")
print("="*60)

y_pred = model_pipe.predict(x_test)

print(f"최종 분류 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[상세 분류 보고서]")
print(classification_report(y_test, y_pred, target_names=faces.target_names))

# =========================================================================
# [STEP 5] 결과 시각화 (Visualization)
# =========================================================================
print("\n" + "="*70)
print("[STEP 5] 예측 결과 및 혼동 행렬 시각화")
print("="*60)

fig, axes = plt.subplots(4, 6)
for i, ax in enumerate(axes.flat):
    ax.imshow(x_test[i].reshape(62, 47), cmap='bone')
    ax.set(xticks=[], yticks=[])
    ax.set_ylabel(faces.target_names[y_pred[i]].split()[-1], color='blue' if y_pred[i] == y_test[i] else 'red')

fig.suptitle("예측 결과", fontsize=12)
plt.tight_layout()
plt.show()

# 1. 오차 행렬(Confusion Matrix) 시각화
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', xticklabels=faces.target_names, yticklabels=faces.target_names)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# 2. PCA 누적 분산 그래프 (정보 유지량 확인)
plt.plot(np.cumsum(m_pca.explained_variance_ratio_))
plt.xlabel("주성분 개수")
plt.ylabel("누적 분산 비율")
plt.title("PCA 누적 분산 비율")
plt.grid(True)
plt.show()
plt.close()


# =========================================================================
# [STEP 6] 실습: 새로운 데이터 예측 (Prediction)
# =========================================================================
print("\n" + "="*70)
print("[STEP 6] 새로운 이미지 데이터를 활용한 분류 테스트")
print("="*60)
print("\n[실습 1] 기존 데이터셋의 샘플 활용")
print("-" * 40)
test_img = faces.data[0].reshape(1, -1) 
print(f"테스트 이미지 데이터(일부): {test_img[0][:5]}...")

test_pred = model_pipe.predict(test_img)
print(f"예측 결과: {faces.target_names[test_pred[0]]} (Index: {test_pred[0]})")
print(f"실제 정답: {faces.target_names[faces.target[0]]}")

# ===========================================================================

print("\n[실습 2] 외부 이미지 파일 활용")
print("-" * 40)
# 이미지 읽기 -> 흑백 변환 -> 크기 맞추기 -> 1차원으로 변환 -> 예측
from PIL import Image

img = Image.open("bush.jpeg").convert("L") # 흑백(Luminance) 변환
img = img.resize((47, 62))                 # 모델 학습 크기(47x62)로 리사이징

"""
[참고] 이미지 배열 구조
- numpy 이미지는 (height, width) 순서
- PIL 이미지는 (width, height) 순서로 처리됨

[주의사항]
1. 데이터 형식 일치: 원본 데이터(faces.data)는 0~255 사이의 픽셀값이 
    float32 형식으로 정규화되어 있거나 특정 스케일을 가질 수 있음.
2. 정규화(Scaling): PIL로 읽어온 이미지(0~255, uint8)를 모델이 학습한 
    데이터 분포와 맞추기 위해 255로 나누거나(MinMax) 스케일링이 필요함.
3. 차원 변형: 2차원 이미지 배열을 1차원(1, 2914)으로 flatten 해야 예측 가능함.
"""

print("\n[3. 이미지 전처리 및 예측 수행]")
img_np = np.array(img).reshape(1, -1) / 255.0 # 1차원 변환 및 정규화(0~1)
print(f"외부 이미지 로드 완료 (구조: {img_np.shape})")

new_pred = model_pipe.predict(img_np)
print(f"외부 이미지 예측 결과: {faces.target_names[new_pred[0]]}")

# 시각화 & 예측
plt.imshow(img, cmap='bone')
plt.title(f"예측 결과: {faces.target_names[new_pred[0]]}")
plt.axis("off")
plt.show()
plt.close()
