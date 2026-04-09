import os
os.system('cls')

from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets

# ex) 성별에 따른 키, 머리카락 데이터

# =========================================================================
#                       분류용 가상 데이터 생성
# =========================================================================
x = [[180, 15], [177, 42], [156, 35], [174, 65], [161, 25]]
y = ["man", "woman","woman", "man", "woman"]
feature_names = ["height", "hair length"]
class_names = ["man", "woman"]

# =========================================================================
#                       모델 생성 및 성능 확인
# =========================================================================
model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
model.fit(x, y)

print(f"정확도 : ", model.score(x, y))
print("예측값 : ", model.predict(x))
print("실제값 : ", y)
print()

# =========================================================================
#                       예측할 데이터
# =========================================================================
new_data = [[177, 78]]
print("새로운 데이터의 예측값 : ", model.predict(new_data))
print()

plt.figure(figsize=(10, 6))
plot_tree(model, feature_names=feature_names, class_names=class_names, filled=True)
plt.show()
plt.close()

