# 스팸 메일 분류기

import os
os.system('cls')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import koreanize_matplotlib


df = pd.read_csv("spam.csv", encoding="latin-1")
print(df.head(3))

df["label"] = df["v1"].str.strip().str.lower()
texts = df["v2"].tolist()
labels = df["label"].tolist()

x_train, x_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=42, stratify=labels)

# 벡터화
vectorizer = CountVectorizer()
x_train_vec = vectorizer.fit_transform(x_train)
x_test_vec = vectorizer.transform(x_test)

# 모델 생성 및 학습
model = MultinomialNB()
model.fit(x_train_vec, y_train)

# 예측
y_pred = model.predict(x_test_vec)

# 평가
accuracy = accuracy_score(y_test, y_pred)
print("Classification Accuracy:", accuracy)
print()

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)
print()

# Classification Report
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.show()
print()

# 사용자 입력 메일 내용 분류
while True:
    userInput = input("메일 내용을 입력하세요 (종료하려면 'q'를 입력하세요): ")
    if userInput.lower() == 'q':
        break
    user_input_vec = vectorizer.transform([userInput])
    prediction = model.predict_proba(user_input_vec)[0]

    spam_prob = prediction[model.classes_.tolist().index("spam")]
    result = "스팸이에요" if spam_prob > 0.7 else "스팸이 아니에요"
    print(result)

    print("분류 결과:", prediction[0])
    print()
