import os
os.system('cls')

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import koreanize_matplotlib

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
vect = CountVectorizer()
x = vect.fit_transform(texts)

model = MultinomialNB()
model.fit(x, labels)

# ------ Stream LIT ------------------
import streamlit as st

st.title("이메일 분류기(Naive Bayes)")

user_input = st.text_input("이메일 내용을 입력하세요")

if user_input:
    x_new = vect.transform([user_input])
    prediction = model.predict(x_new)[0]
    prob = model.predict_proba(x_new)[0]
    
    spam_idx = model.classes_.tolist().index("spam")
    ham_idx = model.classes_.tolist().index("ham")
    spam_prob = prob[spam_idx]
    ham_prob = prob[ham_idx]

    st.write("분류 결과:", prediction)
    st.write(f"확률 결과 -->>  spam : {spam_prob:.4f}, ham : {ham_prob:.4f}")