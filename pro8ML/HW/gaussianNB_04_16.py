'''
[GaussanNB 문제] 
독버섯(poisonous)인지 식용버섯(edible)인지 분류
https://www.kaggle.com/datasets/uciml/mushroom-classification
feature는 중요변수를 찾아 선택, label:class
참고 : from xgboost import plot_importance


데이터 변수 설명 : 총 23개 변수가 사용됨.

여기서 종속변수(반응변수)는 class 이고 나머지 22개는 모두 입력변수(설명변수, 예측변수, 독립변수).
변수명 변수 설명
class      edible = e, poisonous = p
cap-shape    bell = b, conical = c, convex = x, flat = f, knobbed = k, sunken = s
cap-surface  fibrous = f, grooves = g, scaly = y, smooth = s
cap-color     brown = n, buff = b, cinnamon = c, gray = g, green = r, pink = p, purple = u, red = e, white = w, yellow = y
bruises        bruises = t, no = f
odor            almond = a, anise = l, creosote = c, fishy = y, foul = f, musty = m, none = n, pungent = p, spicy = s
gill-attachment attached = a, descending = d, free = f, notched = n
gill-spacing close = c, crowded = w, distant = d
gill-size       broad = b, narrow = n
gill-color      black = k, brown = n, buff = b, chocolate = h, gray = g, green = r, orange = o, pink = p, purple = u, red = e, white = w, yellow = y
stalk-shape  enlarging = e, tapering = t
stalk-root    bulbous = b, club = c, cup = u, equal = e, rhizomorphs = z, rooted = r, missing = ?
stalk-surface-above-ring fibrous = f, scaly = y, silky = k, smooth = s
stalk-surface-below-ring fibrous = f, scaly = y, silky = k, smooth = s
stalk-color-above-ring brown = n, buff = b, cinnamon = c, gray = g, orange = o, pink = p, red = e, white = w, yellow = y
stalk-color-below-ring brown = n, buff = b, cinnamon = c, gray = g, orange = o,pink = p, red = e, white = w, yellow = y
veil-type      partial = p, universal = u
veil-color     brown = n, orange = o, white = w, yellow = y
ring-number none = n, one = o, two = t
ring-type     cobwebby = c, evanescent = e, flaring = f, large = l, none = n, pendant = p, sheathing = s, zone = z
spore-print-color black = k, brown = n, buff = b, chocolate = h, green = r, orange =o, purple = u, white = w, yellow = y
population abundant = a, clustered = c, numerous = n, scattered = s, several = v, solitary = y
habitat       grasses = g, leaves = l, meadows = m, paths = p, urban = u, waste = w, woods = d
'''

import os
os.system('cls')

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import koreanize_matplotlib
from xgboost import plot_importance

# 데이터 로드
data = pd.read_csv('mushrooms.csv')
# print(data.head(3))

# 데이터 전처리
feature = data.drop("class", axis=1)
label = data["class"]

# 데이터 분할 (Train / Test samples)
x_train, x_test, y_train, y_test = train_test_split(feature, label, test_size=0.2, random_state=42, stratify=label)

# regression 모델 생성
model = GaussianNB()
model.fit(x_train, y_train)

# 예측 및 평가
pred = model.predict(x_test)
print(f"테스트 데이터 예측값(10개): {pred[:10]}")
print(f"테스트 데이터 실제값(10개): {y_test[:10].values}")
print(f"최종 분류 정확도: {accuracy_score(y_test, pred):.4f}")

