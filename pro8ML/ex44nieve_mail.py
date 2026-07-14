"""
Naive Bayes(나이브 베이즈) - 스팸 메일 분류 실습
---------------------------------------------------------------------------------------------------
1. 개요 (Overview): 
    - MultinomialNB(다항 나이브 베이즈)를 활용한 텍스트 분류
    - 단어의 출현 빈도(Frequency)를 기반으로 문서가 특정 클래스(Spam/Ham)에 속할 확률을 계산

2. 주요 기법 (Key Techniques):
    - CountVectorizer: 텍스트 데이터를 단어 빈도수 벡터(Bag of Words)로 변환
    - MultinomialNB: 이산적 특징(단어 횟수)을 가진 데이터 분류에 최적화된 알고리즘
---------------------------------------------------------------------------------------------------
"""

import os
os.system('cls')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.metrics import accuracy_score

# =========================================================================
# [STEP 1] 학습용 데이터 준비 (Training Data)
# =========================================================================
print("="*70)
print("[STEP 1] 학습용 텍스트 데이터 및 레이블 생성")
print("="*60)

texts = [
    "무료 쿠폰 잠금 무료 클릭",
    "한번만 클릭하면 무료",
    "오늘 회의는 2시야",
    "지금 할인 행사 진행 중",
    "회의 자료는 메일로 보내주세요",
    "지금 바로 쿠폰 확인",
    "내일 점심 같이 먹을까"
]

labels = ["spam", "spam", "ham", "spam", "ham", "spam", "ham"]

# =========================================================================
# [STEP 2] 텍스트 벡터화 (Text Vectorization)
"""
[CountVectorizer 옵션 설명]
1. stop_words: 분석에서 제외할 불용어 설정
2. token_pattern: 토큰화 규칙 (기본값은 2글자 이상의 단어)
3. fit_transform(): 단어 사전을 만들고(fit), 문장을 빈도수 행렬로 변환(transform)
"""
# =========================================================================
print("\n" + "="*70)
print("[STEP 2] CountVectorizer를 이용한 단어 빈도수 벡터화")
print("="*60)

count_to_vector = CountVectorizer()
x = count_to_vector.fit_transform(texts)

print(f"추출된 단어 사전(Feature Names):\n{count_to_vector.get_feature_names_out()}")
print(x)
'''
[희소 행렬(Sparse Matrix) 출력 결과 설명]
1. (row, col): 데이터의 위치 (몇 번째 문장인지, 몇 번째 단어인지)
2. value: 해당 위치의 단어 빈도수
3. 특징: 0이 아닌 유효한 데이터만 저장하여 메모리 효율성을 높임 (CSR 형식)

<Compressed Sparse Row sparse matrix of dtype 'int64'
        with 26 stored elements and shape (7, 23)>
    Coords        Values
    (0, 5)        2
    (0, 14)       1
    (0, 10)       1
    (0, 15)       1
    (1, 5)        1
    (1, 17)       1
    (1, 16)       1
    (2, 8)        1
    (2, 22)       1
    (2, 0)        1
    (3, 12)       1
    (3, 18)       1
    (3, 19)       1
    (3, 13)       1
    (4, 21)       1
    (4, 9)        1
    (4, 4)        1
    (4, 7)        1
    (5, 14)       1
    (5, 12)       1
    (5, 6)        1
    (5, 20)       1
    (6, 2)        1
    (6, 11)       1
    (6, 1)        1
    (6, 3)        1
'''
print(f"\n벡터화된 행렬 구조: \n{x.toarray()}")
print(count_to_vector.vocabulary_)
'''
{'무료': 5, '쿠폰': 14, '잠금': 10, '클릭': 15, '한번만': 17, '클릭하면': 16, '오늘': 8, '회의는': 22, '2시야': 0, '지금': 12, '할인': 18, '행사': 19, '진행': 13, '회의': 21, '자료는': 9, '메일로': 4, '보내주세요': 7, '바로': 6, '확인': 20, '내일': 2, '점심': 11, '같이': 1, '먹을까': 3}
'''

# =========================================================================
# [STEP 3] 모델 생성 및 학습 (Multinomial Naive Bayes)
"""
[MultinomialNB 옵션 설명]
1. alpha: 라플라스 스무딩(Laplace Smoothing) 계수. 
    - 학습 데이터에 없는 단어가 나올 때 확률이 0이 되는 것을 방지 (기본값: 1.0)
2. fit_prior: 클래스 사전 확률을 데이터에서 학습할지 여부
"""
# =========================================================================
print("\n" + "="*70)
print("[STEP 3] MultinomialNB 모델 학습")
print("="*60)

model = MultinomialNB()
model.fit(x, labels)
print("스팸 분류 모델 학습 완료")

# =========================================================================
# [STEP 4] 새로운 데이터 예측 (Prediction)
# =========================================================================
print("\n" + "="*70)
print("[STEP 4] 새로운 메일 데이터 스팸 여부 예측")
print("="*60)

test_texts = ["무료 쿠폰 지급 발급", "간부 회의는 언제 시작하나요"]

# 새로운 데이터도 반드시 학습 때 사용한 vectorizer로 변환해야 함
x_test = count_to_vector.transform(test_texts)
preds = model.predict(x_test)
probs = model.predict_proba(x_test)

class_names = model.classes_        # ["ham", "spam"]

for text, pred, prob in zip(test_texts, preds, probs):
    # print(f"메일 내용: {text}")
    # print(f"분류 결과: [{'스팸' if p == 'spam' else '정상'}] (확률: {max(prob):.4f})")
    # print("-" * 40)
    prob_str = ", ".join([f"{cls}: {p:.4f}" for cls, p in zip(class_names, prob)])
    print(f"메일 내용: {text}")
    print(f"분류 결과: [{pred}] (확률: {prob_str})")
    print("-" * 40)
print("="*60)


