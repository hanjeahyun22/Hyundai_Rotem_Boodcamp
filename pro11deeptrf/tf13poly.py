# 다항 회귀
# 광고비와 매출의 관계가 직선이 아니라 곡선 형태의 자료

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.system("cls")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import tensorflow as tf

np.random.seed(7)
tf.random.set_seed(7)

# =========================================================================
# [STEP 1] 데이터 생성
# =========================================================================

ad_cost = np.linspace(0, 100, 80)

sales = (
    ad_cost ** 2 * -0.06
    + 7.5 * ad_cost
    + 40
    + np.random.normal(0, 25, size=len(ad_cost))
)

df = pd.DataFrame({
    "광고비": ad_cost,
    "매출": sales
})

print(df.head(2))

df.to_csv("ad_sales.csv", index=False, encoding="utf-8-sig")

# =========================================================================
# [STEP 2] CSV 읽기
# =========================================================================

df = pd.read_csv("ad_sales.csv", encoding="utf-8-sig")
df = df.dropna()

x = df[["광고비"]].values.astype(np.float32)
y = df[["매출"]].values.astype(np.float32)

# =========================================================================
# [STEP 3] 산점도
# =========================================================================

plt.figure(figsize=(8, 5))
plt.scatter(x, y, alpha=0.8)
plt.title("광고비와 매출의 관계")
plt.xlabel("광고비")
plt.ylabel("매출")
plt.grid(True)
plt.show()

# =========================================================================
# [STEP 4] train / test split
# =========================================================================

indices = np.arange(len(x))
np.random.shuffle(indices)

x = x[indices]
y = y[indices]

train_size = int(len(x) * 0.8)

x_train = x[:train_size]
y_train = y[:train_size]

x_test = x[train_size:]
y_test = y[train_size:]

print("x : \n", x_train.shape, x_test.shape)
print("y : \n", y_train.shape, y_test.shape)

# =========================================================================
# [STEP 5] x, y Scaling
# =========================================================================

# x scaling
x_mean = x_train.mean()
x_std = x_train.std()

x_train_scaled = (x_train - x_mean) / x_std
x_test_scaled = (x_test - x_mean) / x_std

# y scaling
# TensorFlow 모델이 더 안정적으로 학습되도록 y도 scaling
y_mean = y_train.mean()
y_std = y_train.std()

y_train_scaled = (y_train - y_mean) / y_std
y_test_scaled = (y_test - y_mean) / y_std

# =========================================================================
# [STEP 6] 다항 특성 생성
# =========================================================================

def make_poly_features(x_scaled, degree=2):
    features = [x_scaled ** i for i in range(1, degree + 1)]
    return np.concatenate(features, axis=1).astype(np.float32)


x_train_poly = make_poly_features(x_train_scaled, degree=2)
x_test_poly = make_poly_features(x_test_scaled, degree=2)

print("선형 회귀 입력 shape : ", x_train_scaled.shape)
print("다항 회귀 입력 shape : ", x_train_poly.shape)

# =========================================================================
# [STEP 7] 평가 함수
# =========================================================================

def r2_score_np(y_true, y_pred):
    ss_res = np.sum(np.square(y_true - y_pred))
    ss_tot = np.sum(np.square(y_true - np.mean(y_true)))
    return 1 - (ss_res / ss_tot)


def evaluate_model(name, y_true, y_pred):
    mse = np.mean(np.square(y_true - y_pred))
    rmse = np.sqrt(mse)
    r2 = r2_score_np(y_true, y_pred)

    print(f"\n[{name}]")
    print(f"MSE : {mse:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"R^2 : {r2:.3f}")


# =========================================================================
# [STEP 8] 선형회귀 모델
# =========================================================================

linear_model = tf.keras.models.Sequential([
    tf.keras.Input(shape=(1,)),
    tf.keras.layers.Dense(1)
])

linear_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    loss="mse"
)

linear_model.fit(
    x_train_scaled,
    y_train_scaled,
    epochs=3000,
    verbose=0
)

# y는 scaling해서 학습했으므로 예측값을 다시 매출 단위로 복원
y_pred_linear_scaled = linear_model.predict(x_test_scaled, verbose=0)
y_pred_linear = y_pred_linear_scaled * y_std + y_mean

evaluate_model("Linear Regression", y_test, y_pred_linear)

# =========================================================================
# [STEP 9] 다항회귀 모델
# =========================================================================

poly_model = tf.keras.models.Sequential([
    tf.keras.Input(shape=(2,)),
    tf.keras.layers.Dense(1)
])

poly_model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    loss="mse"
)

poly_model.fit(
    x_train_poly,
    y_train_scaled,
    epochs=3000,
    verbose=0
)

y_pred_poly_scaled = poly_model.predict(x_test_poly, verbose=0)
y_pred_poly = y_pred_poly_scaled * y_std + y_mean

evaluate_model("Polynomial Regression", y_test, y_pred_poly)

# =========================================================================
# [STEP 10] 최종 성능 비교
# =========================================================================

print("\n" + "=" * 60)
print("[최종 성능 비교]")
print("=" * 60)

evaluate_model("선형 회귀", y_test, y_pred_linear)
evaluate_model("비선형 회귀 degree=2", y_test, y_pred_poly)

# =========================================================================
# [STEP 11] 예측 결과 시각화
# =========================================================================

x_plot = np.linspace(0, 100, 300).reshape(-1, 1).astype(np.float32)

x_plot_scaled = (x_plot - x_mean) / x_std
x_plot_poly = make_poly_features(x_plot_scaled, degree=2)

y_plot_linear_scaled = linear_model.predict(x_plot_scaled, verbose=0)
y_plot_poly_scaled = poly_model.predict(x_plot_poly, verbose=0)

# 매출 복원
y_plot_linear = y_plot_linear_scaled * y_std + y_mean
y_plot_poly = y_plot_poly_scaled * y_std + y_mean

plt.figure(figsize=(9, 6))
plt.scatter(x_train, y_train, alpha=0.5, label="학습 데이터")
plt.scatter(x_test, y_test, alpha=0.9, label="테스트 데이터")
plt.plot(x_plot, y_plot_linear, label="선형 회귀 예측선")
plt.plot(x_plot, y_plot_poly, label="다항 회귀 degree=2 예측선")
plt.title("선형 회귀 vs 다항 회귀")
plt.xlabel("광고비")
plt.ylabel("매출")
plt.grid(True)
plt.legend()
plt.show()